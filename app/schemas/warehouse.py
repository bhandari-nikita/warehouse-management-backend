from pydantic import BaseModel

class WarehouseCreate(BaseModel):
    name: str
    location: str

class WarehouseResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True