from app.models.category import Category
from app.models.product import Product


def test_create_product(client, db):
    category = Category(
        name="Drinks",
        description="Beverages",
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    response = client.post(
        "/products/",
        json={
            "name": "Coca Cola",
            "description": "Cold drink",
            "price": 3.50,
            "stock_quantity": 25,
            "category_id": category.id,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Coca Cola"
    assert data["price"] == 3.50
    assert data["stock_quantity"] == 25
    assert data["category_id"] == category.id


def test_create_product_invalid_category(client):
    response = client.post(
        "/products/",
        json={
            "name": "Invalid Product",
            "description": "Should fail",
            "price": 10,
            "stock_quantity": 5,
            "category_id": 9999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_list_products(client, db):
    category = Category(name="Food")
    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Burger",
        description="Beef burger",
        price=12.50,
        stock_quantity=10,
        category_id=category.id,
    )

    db.add(product)
    db.commit()

    response = client.get("/products/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Burger"
    assert data[0]["stock_quantity"] == 10


def test_get_product(client, db):
    category = Category(name="Desserts")
    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Ice Cream",
        price=5,
        stock_quantity=8,
        category_id=category.id,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.get(f"/products/{product.id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Ice Cream"


def test_get_missing_product(client):
    response = client.get("/products/9999")

    assert response.status_code == 404
