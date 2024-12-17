#!/usr/bin/python3


from fastapi import APIRouter
from typing import List
from ..schemas.requests.order import OrderRead
from ..managers.order_manager import OrderManager


router = APIRouter(prefix="", tags=["Orders Resource"])


@router.post("/", response_model=OrderRead)
async def create_order(order):
    """This sends the order data sent from the frontend to the OrderManager for processing and validations"""
    return await OrderManager.create_order(order)


# Get Order
@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id):
    """Retrieve an order by its ID."""
    return await OrderManager.get_order(order_id)


# List Orders
@router.get("/", response_model=List[OrderRead])
async def list_orders():
    """List all orders."""
    return await OrderManager.list_orders()


# Append Items to Order
@router.patch("/{order_id}/items/append")
async def append_order_items(order_id, items_to_add):
    """Append items to the order's items list and recalculate total price."""
    return await OrderManager.append_order_items(order_id, items_to_add)


# Update Specific Item in Order
@router.patch("/{order_id}/items/update")
async def update_order_item(order_id, old_item_name, new_item):
    """Update a specific item in the order's items list and recalculate total price."""
    return await OrderManager.update_order_item(order_id, old_item_name, new_item)


# Remove Specific Item from Order
@router.patch("/{order_id}/items/remove")
async def remove_order_item(order_id, item_name):
    """Remove a specific item from the order's items list and recalculate total price."""
    return await OrderManager.remove_order_item(order_id, item_name)


# Cancel Order
@router.put("/{order_id}/cancel")
async def cancel_order(order_id):
    """Cancel an order by updating its status."""
    return await OrderManager.cancel_order(order_id)


# Delete Order
@router.delete("/{order_id}")
async def delete_order(order_id):
    """Delete an order by its ID."""
    return await OrderManager.delete_order(order_id)

