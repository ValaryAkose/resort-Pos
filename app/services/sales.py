from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.sales import Sale, SaleItem
from app.models.user import User
from app.schemas.sales import SaleCreate


TAX_RATE = 0.10


def create_sale(
    db: Session,
    data: SaleCreate,
    user: User,
):
    # 1. Validate customer if supplied
    customer = None

    if data.customer_id is not None:
        customer = (
            db.query(Customer)
            .filter(Customer.id == data.customer_id)
            .first()
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

    # 2. Validate payment method
    allowed_payment_methods = {
        "cash",
        "card",
        "room_charge",
    }

    if data.payment_method not in allowed_payment_methods:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment method",
        )

    # 3. Prepare sale items
    sale_items = []
    subtotal = 0.0

    for item_data in data.items:
        product = (
            db.query(Product)
            .filter(Product.id == item_data.product_id)
            .first()
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item_data.product_id} not found",
            )

        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product '{product.name}' is inactive",
            )

        if product.stock_quantity < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Insufficient stock for '{product.name}'. "
                    f"Available: {product.stock_quantity}"
                ),
            )

        item_subtotal = product.price * item_data.quantity
        subtotal += item_subtotal

        sale_items.append(
            {
                "product": product,
                "quantity": item_data.quantity,
                "unit_price": product.price,
                "subtotal": item_subtotal,
            }
        )

    # 4. Calculate totals
    tax = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + tax, 2)

    # 5. Create Sale
    sale = Sale(
        customer_id=data.customer_id,
        user_id=user.id,
        subtotal=round(subtotal, 2),
        tax=tax,
        total=total,
        payment_method=data.payment_method,
        payment_status="paid",
    )

    db.add(sale)
    db.flush()

    # 6. Create SaleItems and reduce stock
    for item in sale_items:
        product = item["product"]

        product.stock_quantity -= item["quantity"]

        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            subtotal=item["subtotal"],
        )

        db.add(sale_item)

    # 7. Save transaction
    db.commit()
    db.refresh(sale)

    return sale
