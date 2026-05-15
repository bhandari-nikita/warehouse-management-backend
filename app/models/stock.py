from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base

class Stock(Base):
    __tablename__ = "stock"

    id = Column (Integer, primary_key=True, index=True)
    product_id = Column (Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column (Integer, ForeignKey("warehouses.id"), nullable=False)
    quantity = Column (Integer, nullable=False)
