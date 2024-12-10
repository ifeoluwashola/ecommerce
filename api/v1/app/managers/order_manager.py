from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy.orm.attributes import flag_modified


from ..schemas.resquests.orders import OrderRead, OrderCreate, Item
from ..schemas.responses.custom_responses import NOTFOUND
from ..models.order_model import Order as OrderModel, OrderStatus
from ...database.db import get_db


class OrderManager:
    """This will handle the orders related logic and database transactions"""
    @staticmethod
    async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
        """Create a new order. Total price is calculated automatically."""
        # Calculate total price
        total_price = sum(item.price for item in order.items)

        # Create the order
        db_order = OrderModel(
            customer_id=order.customer_id,
            items=[item.dict() for item in order.items],  # Convert Pydantic models to dictionaries
            total_price=total_price
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    async def get_order(order_id: UUID, db: Session = Depends(get_db)):
        """Retrieve an order by its ID."""
        order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail=NOTFOUND)
        return order

    @staticmethod
    async def list_orders(db: Session = Depends(get_db)):
        """List all orders."""
        orders = db.query(OrderModel).all()
        return orders

    # Append Items to Order
    @staticmethod
    async def append_order_items(order_id: UUID, items_to_add: List[Item], db: Session = Depends(get_db)):
        """Append items to the order's items list and recalculate total price."""
        order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail=NOTFOUND)

        # Append new items
        order.items.extend(item.dict() for item in items_to_add)
        order.total_price = sum(item["price"] for item in order.items)  # Recalculate total price

        flag_modified(order, "items")
        db.commit()
        db.refresh(order)
        return {"message": "Items appended successfully", "order": order}

    # Update Specific Item in Order
    @staticmethod
    async def update_order_item(
            order_id: UUID,
            old_item_name: str,
            new_item: Item,
            db: Session = Depends(get_db)
    ):
        """Update a specific item in the order's items list and recalculate total price."""
        order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail=NOTFOUND)

        # Find the item to update
        item_to_update = next((item for item in order.items if item["name"] == old_item_name), None)
        if not item_to_update:
            raise HTTPException(status_code=400, detail=f"Item '{old_item_name}' not found in order")

        # Update the item
        item_to_update.update(new_item.dict())
        order.total_price = sum(item["price"] for item in order.items)  # Recalculate total price

        flag_modified(order, "items")
        db.commit()
        db.refresh(order)
        return {"message": f"Item '{old_item_name}' updated successfully", "order": order}

    # Remove Specific Item from Order
    @staticmethod
    async def remove_order_item(order_id: UUID, item_name: str, db: Session = Depends(get_db)):
        """Remove a specific item from the order's items list and recalculate total price."""
        order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail=NOTFOUND)

        # Find the item to remove
        item_to_remove = next((item for item in order.items if item["name"] == item_name), None)
        if not item_to_remove:
            raise HTTPException(status_code=400, detail=f"Item '{item_name}' not found in order")

        # Remove the item
        order.items.remove(item_to_remove)
        order.total_price = sum(item["price"] for item in order.items)  # Recalculate total price

        flag_modified(order, "items")
        db.commit()
        db.refresh(order)
        return {"message": f"Item '{item_name}' removed successfully", "order": order}

    # Cancel Order
    @staticmethod
    async def cancel_order(order_id: UUID, db: Session = Depends(get_db)):
        """Cancel an order by updating its status."""
        order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail=NOTFOUND)
        if order.status == OrderStatus.CANCELED:
            raise HTTPException(status_code=400, detail="Order is already canceled")
        order.status = OrderStatus.CANCELED
        db.commit()
        db.refresh(order)
        return {"message": "Order canceled successfully", "order": order}

    # Delete Order
    @staticmethod
    async def delete_order(order_id: UUID, db: Session = Depends(get_db)):
        """Delete an order by its ID."""
        order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail=NOTFOUND)
        db.delete(order)
        db.commit()
        return {"message": "Order deleted successfully"}


