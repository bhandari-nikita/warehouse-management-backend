from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.models.warehouse import Warehouse
from app.schemas.warehouse import (WarehouseCreate, WarehouseResponse)

router = APIRouter (prefix="/warehouses", tags=["Warehouses"])

@router.post("/", response_model=WarehouseResponse)
def create_warehouse (
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db)
):
    new_warehouse = Warehouse (
        name = warehouse.name,
        location = warehouse.location
    )

    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)

    return new_warehouse

@router.get("/", response_model=list[WarehouseResponse])
def get_warehouse (db: Session = Depends(get_db)):
    warehouses = db.query(Warehouse).all()

    return warehouses
