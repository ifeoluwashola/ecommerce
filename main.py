from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from api.v1.app.router.routers import api_router
ORIGINS = [
    "http://localhost",
    "http://localhost:8000"
]


app = FastAPI()
app.include_router(api_router)
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

