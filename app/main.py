from fastapi import FastAPI

from app.routers.category import router as category_router
from app.routers.customer import router as customer_router
from app.routers.product import router as product_router
from app.routers.user import router as user_router
from app.routers.sales import router as sales_router


app = FastAPI(
    title="Resort POS API",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Resort POS API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(user_router)
app.include_router(category_router)
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(sales_router)
