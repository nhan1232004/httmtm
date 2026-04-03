from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
async def read_products():
    return [
        {"id": 1, "name": "Product 1"},
        {"id": 2, "name": "Product 2"},
    ]

@app.get("/recommendations")
async def read_recommendations():
    return [
        {"id": 1, "product_id": 1, "recommendation": "Recommended Product A"},
        {"id": 2, "product_id": 2, "recommendation": "Recommended Product B"},
    ]