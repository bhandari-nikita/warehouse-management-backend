from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate

def create_product_service(
        product: ProductCreate,
        db: Session   # Tells Python/IDE: "db variable will contain SQLAlchemy Session object"
):
    
    new_product = Product(
        name=product.name,
        sku=product.sku,
        description=product.description,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product