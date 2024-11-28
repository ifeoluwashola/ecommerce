from fastapi import FastAPI
from routers import orders
from database import engine
from models import Base
import uvicorn

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Order Service",
    description="A microservice to manage E-commerce orders.",
    version="1.0.0"
)

app.include_router(orders.router, prefix="/orders", tags=["Orders"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Order Service!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)