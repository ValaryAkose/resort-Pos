from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category import (
    add_category,
    edit_category,
    find_category,
    list_categories,
    remove_category,
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get(
    "/",
    response_model=list[CategoryResponse],
)
def get_all_categories(
    db: Session = Depends(get_db),
):
    return list_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_one_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    return find_category(db, category_id)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
):
    return add_category(db, data)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_existing_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    return edit_category(db, category_id, data)


@router.delete("/{category_id}")
def delete_existing_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    return remove_category(db, category_id)
