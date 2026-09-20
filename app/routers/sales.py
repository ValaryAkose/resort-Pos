from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.sales import SaleCreate, SaleResponse
from app.services.sales import create_sale


router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


@router.post(
    "/",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_sale(
        db=db,
        data=data,
        user=current_user,
    )
