from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: str
    price: float

class ProductResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True   # Allows Pydantic to convert SQLAlchemy objects into JSON responses.
