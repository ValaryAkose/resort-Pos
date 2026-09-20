from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_categories(db: Session):
    return db.query(Category).all()


def get_category(db: Session, category_id: int):
    return (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )


def get_category_by_name(db: Session, name: str):
    return (
        db.query(Category)
        .filter(Category.name == name)
        .first()
    )


def create_category(db: Session, data: CategoryCreate):
    category = Category(
        name=data.name,
        description=data.description,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def update_category(
    db: Session,
    category: Category,
    data: CategoryUpdate,
):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()
