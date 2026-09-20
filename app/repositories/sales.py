from sqlalchemy.orm import Session

from app.models.sales import Sale


def get_sales(db: Session):
    return (
        db.query(Sale)
        .order_by(Sale.created_at.desc())
        .all()
    )


def get_sale(db: Session, sale_id: int):
    return (
        db.query(Sale)
        .filter(Sale.id == sale_id)
        .first()
    )
