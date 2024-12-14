#!/usr/bin/python3

from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from api.v1.app.router.routers import api_router
ORIGINS = [
    "http://localhost",
    "http://localhost:8000"
]


app = FastAPI(title="MartPlaza Backend")
app.include_router(api_router)


@app.get("/")
async def index():
    return {
        "message": "MartPlaza, is a work in progress, give us some time."
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    # added the app as "main:app" to be able to reload automatically on any changes.
    uvicorn.run("main:app", reload=True)

