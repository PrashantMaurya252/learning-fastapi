from fastapi import FastAPI,HTTPException
from app.service.products import get_all_product

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Welcome to FASTAPI"}

@app.get("/products/{id}")
def get_product(id:int):
    products = ["Brush","Pencil","Book","Pen"]
    if(id < 0 or id >= len(products)):
        raise HTTPException(status_code=404,detail="Product not found")

    return products[id]

@app.get("/products")
def get_all_products():
    return get_all_product()