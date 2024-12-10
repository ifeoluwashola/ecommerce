from fastapi import APIRouter

from ..resources import order_resource

api_router = APIRouter()

api_router.include_router(order_resource.router)

