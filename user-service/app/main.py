from fastapi import FastAPI, Request
from app.routes import user_router
from app.db import Base, engine
import uvicorn
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service",
    description="A microservice to manage E-commerce Users.",
    version="1.0.0"
)

app.include_router(user_router, prefix="/api/users", tags=["Users"])
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
async def root():
    return {"message": "Welcome to the User Service!"}

@app.get("/login")
@limiter.limit("5/minute")
async def login(request: Request):
    return {"message": "Login endpoint"}

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002)