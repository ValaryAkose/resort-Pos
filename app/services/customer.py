from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.customer import (
    create_customer,
    delete_customer,
    get_customer,
    get_customers,
    update_customer,
)
from app.schemas.customer import CustomerCreate, CustomerUpdate


def list_customers(db: Session):
    return get_customers(db)


def find_customer(db: Session, customer_id: int):
    customer = get_customer(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


def add_customer(db: Session, data: CustomerCreate):
    return create_customer(db, data)


def edit_customer(
    db: Session,
    customer_id: int,
    data: CustomerUpdate,
):
    customer = find_customer(db, customer_id)

    return update_customer(db, customer, data)


def remove_customer(db: Session, customer_id: int):
    customer = find_customer(db, customer_id)

    delete_customer(db, customer)

    return {
        "message": "Customer deleted successfully"
    }
