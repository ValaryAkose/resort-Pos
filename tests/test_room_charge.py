from app.core.security import hash_password
from app.models.category import Category
from app.models.customer import Customer
from app.models.product import Product
from app.models.user import User


def setup_room_charge_data(db):
    user = User(
        username="roomcashier",
        password_hash=hash_password("password123"),
        role="cashier",
        is_active=True,
    )

    category = Category(name="Room Charge Food")

    customer = Customer(
        name="Resort Guest",
        room_number="305",
        phone="0700000000",
    )

    db.add_all([user, category, customer])
    db.commit()

    db.refresh(category)
    db.refresh(customer)

    product = Product(
        name="Room Service Meal",
        price=25.00,
        stock_quantity=10,
        category_id=category.id,
        is_active=True,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return user, customer, product


def test_room_charge_sale(client, db):
    _, customer, product = setup_room_charge_data(db)

    login = client.post(
        "/auth/login",
        json={
            "username": "roomcashier",
            "password": "password123",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        "/sales/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "customer_id": customer.id,
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 1,
                }
            ],
            "payment_method": "room_charge",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer_id"] == customer.id
    assert data["payment_method"] == "room_charge"
    assert data["payment_status"] == "paid"

    assert data["subtotal"] == 25.00
    assert data["tax"] == 2.50
    assert data["total"] == 27.50


def test_cash_sale_with_customer(client, db):
    _, customer, product = setup_room_charge_data(db)

    login = client.post(
        "/auth/login",
        json={
            "username": "roomcashier",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        "/sales/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "customer_id": customer.id,
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 1,
                }
            ],
            "payment_method": "cash",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer_id"] == customer.id
    assert data["payment_method"] == "cash"
