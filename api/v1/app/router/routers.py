#!/usr/bin/python3


from fastapi import APIRouter

from ..resources import order_resource, product_resource, user_resources, auth

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(user_resources.router)

# api_router.include_router(order_resource.router)
# api_router.include_router(product_resource.router)
