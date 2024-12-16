#!/usr/bin/python3


from typing import List

from pydantic import BaseModel
from uuid import UUID

from ...models.order_model import OrderStatus


# Pydantic schemas for request and response
class Item(BaseModel):
    name: str
    price: float


class OrderCreate(BaseModel):
    customer_id: UUID
    items: List[Item]  # List of items with name and price


class OrderRead(BaseModel):
    order_id: UUID
    customer_id: UUID
    items: List[Item]
    total_price: float
    status: OrderStatus
