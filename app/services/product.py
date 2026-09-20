from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.repositories.product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product,
)
from app.schemas.product import ProductCreate, ProductUpdate


def list_products(db: Session):
    return get_products(db)


def find_product(db: Session, product_id: int):
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


def add_product(db: Session, data: ProductCreate):
    category = (
        db.query(Category)
        .filter(Category.id == data.category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return create_product(db, data)


def edit_product(
    db: Session,
    product_id: int,
    data: ProductUpdate,
):
    product = find_product(db, product_id)

    if data.category_id is not None:
        category = (
            db.query(Category)
            .filter(Category.id == data.category_id)
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

    return update_product(db, product, data)


def remove_product(db: Session, product_id: int):
    product = find_product(db, product_id)

    delete_product(db, product)

    return {
        "message": "Product deleted successfully"
    }
