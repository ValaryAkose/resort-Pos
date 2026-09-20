from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    room_number = Column(String(50), nullable=True)
    phone = Column(String(30), nullable=True)

    sales = relationship(
        "Sale",
        back_populates="customer",
    )
