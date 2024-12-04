from fastapi import FastAPI
from app.db import Base, engine
from app.routes import product_router
import uvicorn
# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Service",
    description="A microservice to manage E-commerce Products.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(product_router, prefix="/api/products", tags=["Products"])

@app.get("/")
def root():
    return {"message": "Welcome to the Product Service!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)