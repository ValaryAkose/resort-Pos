from app.core.security import hash_password
from app.models.category import Category
from app.models.product import Product
from app.models.user import User


def test_sale_with_multiple_products(client, db):
    user = User(
        username="multicashier",
        password_hash=hash_password("password123"),
        role="cashier",
        is_active=True,
    )
    db.add(user)

    category = Category(name="Multiple Items")
    db.add(category)

    db.commit()
    db.refresh(category)

    burger = Product(
        name="Burger",
        price=10.00,
        stock_quantity=20,
        category_id=category.id,
        is_active=True,
    )

    juice = Product(
        name="Orange Juice",
        price=5.00,
        stock_quantity=20,
        category_id=category.id,
        is_active=True,
    )

    db.add_all([burger, juice])
    db.commit()

    db.refresh(burger)
    db.refresh(juice)

    login = client.post(
        "/auth/login",
        json={
            "username": "multicashier",
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
            "items": [
                {
                    "product_id": burger.id,
                    "quantity": 2,
                },
                {
                    "product_id": juice.id,
                    "quantity": 3,
                },
            ],
            "payment_method": "cash",
        },
    )

    assert response.status_code == 201

    data = response.json()

    # 2 × 10 + 3 × 5 = 35
    assert data["subtotal"] == 35.00

    # Current POS tax rule: 10%
    assert data["tax"] == 3.50

    assert data["total"] == 38.50

    assert len(data["items"]) == 2

    db.refresh(burger)
    db.refresh(juice)

    assert burger.stock_quantity == 18
    assert juice.stock_quantity == 17
