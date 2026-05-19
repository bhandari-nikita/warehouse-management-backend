from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.product import Product
from app.schemas.product import (ProductCreate, ProductResponse)

from app.services.product_service import (create_product_service)

from app.core.security import require_role


router = APIRouter (prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def get_products(
    min_price: float = 0,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.price >= min_price
    ).offset(offset).limit(limit).all()

    return products


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db) # FastAPI automatically provides a database session using dependency injection.
):
    return create_product_service(product, db)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code = 404,
            detail = "Product not found"
        )
    
    product.name = updated_product.name,
    product.sku = updated_product.sku,
    product.description = updated_product.description,
    product.price = updated_product.price

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code = 404,
            detail = "Product not found"
        )
    
    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}


