from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.schemas.transfer import StockTransfer

from app.models.stock import Stock

router = APIRouter (prefix="/transfer", tags=["Transfer"])

@router.post("/")
def transfer_stock(
    transfer: StockTransfer,
    db: Session = Depends(get_db)
):
    if transfer.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero."
        )
    
    if (
        transfer.source_warehouse_id
        ==
        transfer.destination_warehouse_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Source and destination warehouses must differ."
        )
    
    source_stock = db.query(Stock).filter(
        Stock.product_id == transfer.product_id,
        Stock.warehouse_id == transfer.source_warehouse_id
    ).first()

    if not source_stock:
        raise HTTPException(
            status_code=404,
            detail="Source stock not found."
        )
    
    if source_stock.quantity < transfer.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock in source warehouse."
        )
    
    destination_stock = db.query(Stock).filter(
        Stock.product_id == transfer.product_id,
        Stock.warehouse_id == transfer.destination_warehouse_id
    ).first()

    if not destination_stock:
        destination_stock = Stock(
            product_id = transfer.product_id,
            warehouse_id = transfer.destination_warehouse_id,
            quantity = 0
        )

        db.add(destination_stock)
        
    source_stock.quantity -= transfer.quantity
    destination_stock.quantity += transfer.quantity

    db.commit()

    return {"message": "Stock transfer successful."}
