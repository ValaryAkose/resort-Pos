from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.category import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    get_category_by_name,
    update_category,
)
from app.schemas.category import CategoryCreate, CategoryUpdate


def list_categories(db: Session):
    return get_categories(db)


def find_category(db: Session, category_id: int):
    category = get_category(db, category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


def add_category(db: Session, data: CategoryCreate):
    existing = get_category_by_name(db, data.name)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists",
        )

    return create_category(db, data)


def edit_category(
    db: Session,
    category_id: int,
    data: CategoryUpdate,
):
    category = find_category(db, category_id)

    if data.name:
        existing = get_category_by_name(db, data.name)

        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists",
            )

    return update_category(db, category, data)


def remove_category(db: Session, category_id: int):
    category = find_category(db, category_id)

    delete_category(db, category)

    return {
        "message": "Category deleted successfully"
    }
