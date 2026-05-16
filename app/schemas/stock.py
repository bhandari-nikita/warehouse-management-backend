from pydantic import BaseModel

class StockCreate(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int

class StockResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True