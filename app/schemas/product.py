from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2)
    sku: str = Field(..., min_length=2)
    description: str
    price: float = Field(..., gt=0)  # ... means required, gt=0 means greater than 0

class ProductResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True   # Allows Pydantic to convert SQLAlchemy objects into JSON responses.
