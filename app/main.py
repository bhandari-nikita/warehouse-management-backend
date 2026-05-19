from fastapi import FastAPI
from app.db.database import engine, Base

from app.models.user import User
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.stock import Stock
from app.models.audit_log import AuditLog

from app.api.product import router as product_router
from app.api.warehouse import router as warehouse_router
from app.api.stock import router as stock_router
from app.api.transfer import router as transfer_router
from app.api.auth import router as auth_router

Base.metadata.create_all(bind=engine) #This tells SQLAlchemy: create tables inside PostgreSQL based on model definitions.

app = FastAPI()

app.include_router(product_router)
app.include_router(warehouse_router)
app.include_router(stock_router)
app.include_router(transfer_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API working"}