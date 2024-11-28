from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Order as OrderModel, OrderStatus
from database import get_db
from pydantic import BaseModel
from uuid import UUID
from typing import List, Dict
from sqlalchemy.orm.attributes import flag_modified

# Router
router = APIRouter()

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

NOTFOUND = "Order not found"


# Create Order
@router.post("/", response_model=OrderRead)
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


# Get Order
@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: UUID, db: Session = Depends(get_db)):
    """Retrieve an order by its ID."""
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    return order


# List Orders
@router.get("/", response_model=List[OrderRead])
async def list_orders(db: Session = Depends(get_db)):
    """List all orders."""
    orders = db.query(OrderModel).all()
    return orders


# Append Items to Order
@router.patch("/{order_id}/items/append")
async def append_order_items(
    order_id: UUID,
    items_to_add: List[Item],
    db: Session = Depends(get_db)
):
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
@router.patch("/{order_id}/items/update")
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
@router.patch("/{order_id}/items/remove")
async def remove_order_item(
    order_id: UUID,
    item_name: str,
    db: Session = Depends(get_db)
):
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
@router.put("/{order_id}/cancel")
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
@router.delete("/{order_id}")
async def delete_order(order_id: UUID, db: Session = Depends(get_db)):
    """Delete an order by its ID."""
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
