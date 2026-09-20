from app.core.security import hash_password
from app.models.category import Category
from app.models.product import Product
from app.models.user import User


def create_test_user(db):
    user = User(
        username="salescashier",
        password_hash=hash_password("password123"),
        full_name="Sales Cashier",
        role="cashier",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_token(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "salescashier",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]


def create_product(db, stock=20):
    category = Category(name="Test Food")
    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Test Chicken",
        description="Test product",
        price=10.00,
        stock_quantity=stock,
        category_id=category.id,
        is_active=True,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def test_create_sale(client, db):
    create_test_user(db)
    product = create_product(db, stock=20)

    token = get_token(client)

    response = client.post(
        "/sales/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 2,
                }
            ],
            "payment_method": "cash",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["subtotal"] == 20.0
    assert data["tax"] == 2.0
    assert data["total"] == 22.0
    assert data["payment_method"] == "cash"
    assert data["payment_status"] == "paid"

    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["unit_price"] == 10.0
    assert data["items"][0]["subtotal"] == 20.0

    db.refresh(product)

    assert product.stock_quantity == 18


def test_sale_requires_authentication(client, db):
    product = create_product(db)

    response = client.post(
        "/sales/",
        json={
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 1,
                }
            ],
            "payment_method": "cash",
        },
    )

    assert response.status_code == 401


def test_sale_rejects_insufficient_stock(client, db):
    create_test_user(db)
    product = create_product(db, stock=2)

    token = get_token(client)

    response = client.post(
        "/sales/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 3,
                }
            ],
            "payment_method": "cash",
        },
    )

    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]

    db.refresh(product)

    # Stock must not be changed when the sale fails.
    assert product.stock_quantity == 2


def test_sale_rejects_missing_product(client, db):
    create_test_user(db)

    token = get_token(client)

    response = client.post(
        "/sales/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "items": [
                {
                    "product_id": 9999,
                    "quantity": 1,
                }
            ],
            "payment_method": "cash",
        },
    )

    assert response.status_code == 404
