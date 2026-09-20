from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from app.services.customer import (
    add_customer,
    edit_customer,
    find_customer,
    list_customers,
    remove_customer,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get(
    "/",
    response_model=list[CustomerResponse],
)
def get_all_customers(
    db: Session = Depends(get_db),
):
    return list_customers(db)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_one_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    return find_customer(db, customer_id)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    return add_customer(db, data)


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_existing_customer(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
):
    return edit_customer(db, customer_id, data)


@router.delete("/{customer_id}")
def delete_existing_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    return remove_customer(db, customer_id)
