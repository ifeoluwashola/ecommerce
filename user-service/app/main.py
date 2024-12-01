from fastapi import FastAPI
from app.routes import user_router
from app.db import Base, engine
import uvicorn

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service",
    description="A microservice to manage E-commerce Users.",
    version="1.0.0"
)

app.include_router(user_router, prefix="/api/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the User Service!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002)