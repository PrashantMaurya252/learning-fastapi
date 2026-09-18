from fastapi import FastAPI,HTTPException,Query,Path
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

@app.get("/product")
def product(
    name:str=Query(default=None,min_length=0,max_length=50,description="Search by product name(case insenitive)"),
    sort_by_price:bool=Query(default=False,description="sort product by price"),
    order:str=Query(default='asc',description="sort order when sort_by_order is true (asc,desc)"),
    limit:int=Query(default=5,ge=1,le=100,description="Number of items"),
    offset:int=Query(default=0,ge=0,description="pagination offset")
            ):
    products = get_all_product()
    if name:
        needle = name.strip().lower()
        products= [p for p in products if needle in p.get("name","").lower()]
        if not products:
            raise HTTPException(status_code=404,detail=f"no product found matching name={name}")

        if sort_by_price:
            reverse = order == 'desc'
            products = sorted(products,key=lambda p:p.get("price",0),reverse=reverse)

        total = len(products)
        products=products[offset:limit+offset]

    return{
        "total":total,
        "limit":limit,
        "items":products
    }

@app.get("/product_details/{id}")
def product_details(id:int=Path(...,ge=0,description="UUID of products")):
    products = get_all_product()
    for product in products:
        if product["id"] == id:
            return product
    raise HTTPException(status_code=404,detail="Product not found")