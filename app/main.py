from fastapi import FastAPI
from app.db.database import engine, Base

from app.models.user import User
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.stock import Stock

Base.metadata.create_all(bind=engine) #This tells SQLAlchemy: create tables inside PostgreSQL based on model definitions.

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API working"}