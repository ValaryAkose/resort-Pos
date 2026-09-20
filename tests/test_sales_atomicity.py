from app.core.security import hash_password
from app.models.category import Category
from app.models.product import Product
from app.models.sales import Sale
from app.models.user import User


def test_multi_item_sale_is_atomic(client, db):
    user = User(
        username="atomiccashier",
        password_hash=hash_password("password123"),
        role="cashier",
        is_active=True,
    )

    category = Category(name="Atomic Test Food")

    db.add(user)
    db.add(category)
    db.commit()
    db.refresh(category)

    product_a = Product(
        name="Available Item",
        price=10.00,
        stock_quantity=10,
        category_id=category.id,
        is_active=True,
    )

    product_b = Product(
        name="Limited Item",
        price=20.00,
        stock_quantity=1,
        category_id=category.id,
        is_active=True,
    )

    db.add_all([product_a, product_b])
    db.commit()

    db.refresh(product_a)
    db.refresh(product_b)

    login = client.post(
        "/auth/login",
        json={
            "username": "atomiccashier",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    sales_before = db.query(Sale).count()

    response = client.post(
        "/sales/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "items": [
                {
                    "product_id": product_a.id,
                    "quantity": 2,
                },
                {
                    "product_id": product_b.id,
                    "quantity": 3,
                },
            ],
            "payment_method": "cash",
        },
    )

    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]

    db.refresh(product_a)
    db.refresh(product_b)

    # Nothing should have been deducted.
    assert product_a.stock_quantity == 10
    assert product_b.stock_quantity == 1

    # No incomplete sale should exist.
    sales_after = db.query(Sale).count()
    assert sales_after == sales_before
