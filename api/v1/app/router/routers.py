#!/usr/bin/python3


from fastapi import APIRouter
from ..resources import order_resource, product_resource, user_resources, auth
from ..admin.resources import admin

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(user_resources.router)
api_router.include_router(admin.router)

