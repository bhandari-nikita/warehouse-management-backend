from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.models.stock import Stock
from app.models.product import Product
from app.models.warehouse import Warehouse

from app.schemas.stock import (StockCreate, StockResponse)

router = APIRouter (prefix="/stock", tags=["stock"])

@router.post("/", response_model=StockResponse)
def create_stock(
    stock: StockCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == stock.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    warehouse = db.query(Warehouse).filter(
        Warehouse.id == stock.warehouse_id
    ).first()

    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    new_stock = Stock(
        product_id = stock.product_id,
        warehouse_id = stock.warehouse_id,
        quantity = stock.quantity
    )

    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return new_stock


@router.get("/", response_model=list[StockResponse])
def get_stock(
    db: Session = Depends(get_db)
):
    stock_items = db.query(Stock).all()

    return stock_items