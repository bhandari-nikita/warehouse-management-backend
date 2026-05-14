from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.product import Product

Base.metadata.create_all(bind=engine) #This tells SQLAlchemy: create tables inside PostgreSQL based on model definitions.

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API working"}