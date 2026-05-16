from pydantic import BaseModel

class StockTransfer(BaseModel):
    product_id: int
    source_warehouse_id: int
    destination_warehouse_id: int
    quantity: int