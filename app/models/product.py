from sqlalchemy import Column, Float, Integer, String, Boolean
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column (Integer, primary_key=True, index=True)
    name = Column (String, nullable=False)
    sku = Column (String, unique=True, nullable=False) #Stock Keeping Unit - Example: LAPTOP-HP-001
    description = Column (String)
    price = Column (Float, nullable=False)
    is_deleted = Column (Boolean, default=False)