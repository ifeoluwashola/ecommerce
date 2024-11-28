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

# Helper function
def recalculate_order_total(order: OrderModel):
    """Recalculate the total price of an order based on its items."""
    order.total_price = sum(item.get("price", 0.0) for item in order.items)

# Pydantic schemas
class OrderCreate(BaseModel):
    customer_id: UUID
    items: List[Dict[str, float]]  # List of items with their prices, e.g., {"name": "item1", "price": 50.0}

class OrderRead(OrderCreate):
    order_id: UUID
    status: OrderStatus
    total_price: float


NOTFOUND = "Order not found"


# Create Order
@router.post("/", response_model=OrderRead)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order."""
    # Validate items
    for item in order.items:
        if "name" not in item or "price" not in item:
            raise HTTPException(status_code=400, detail="Each item must include 'name' and 'price'")
        if not isinstance(item["price"], (int, float)) or item["price"] < 0:
            raise HTTPException(status_code=400, detail="Item price must be a non-negative number")

    # Calculate total price
    total_price = sum(item["price"] for item in order.items)

    # Create and save order
    db_order = OrderModel(
        customer_id=order.customer_id,
        items=order.items,
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
    return db.query(OrderModel).all()


# Update Order Status
@router.put("/{order_id}/status", response_model=OrderRead)
async def update_order_status(order_id: UUID, status: OrderStatus, db: Session = Depends(get_db)):
    """Update the status of an order."""
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    order.status = status
    db.commit()
    db.refresh(order)
    return order


# Append Items to Order
@router.patch("/{order_id}/items/append")
async def append_order_items(
    order_id: UUID,
    items_to_add: List[Dict[str, float]],
    db: Session = Depends(get_db)
):
    """Append items to an order."""
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=NOTFOUND)

    # Validate new items
    for item in items_to_add:
        if "name" not in item or "price" not in item:
            raise HTTPException(status_code=400, detail="Each item must include 'name' and 'price'")
        if not isinstance(item["price"], (int, float)) or item["price"] < 0:
            raise HTTPException(status_code=400, detail="Item price must be a non-negative number")

    # Append items and recalculate total price
    order.items.extend(items_to_add)
    recalculate_order_total(order)

    flag_modified(order, "items")
    db.commit()
    db.refresh(order)
    return {"message": "Items appended successfully", "order": order}


# Update Specific Item in Order
@router.patch("/{order_id}/items/update")
async def update_order_item(
    order_id: UUID,
    old_item_name: str,
    new_item: Dict[str, float],
    db: Session = Depends(get_db)
):
    """Update a specific item in the order."""
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=NOTFOUND)

    # Find and replace the item
    item_to_update = next((item for item in order.items if item["name"] == old_item_name), None)
    if not item_to_update:
        raise HTTPException(status_code=400, detail=f"Item '{old_item_name}' not found in order")

    if "price" not in new_item or new_item["price"] < 0:
        raise HTTPException(status_code=400, detail="New item must include a valid 'price'")

    # Update the item and recalculate total price
    item_to_update.update(new_item)
    recalculate_order_total(order)

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
    """Remove an item from the order."""
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=NOTFOUND)

    # Find and remove the item
    item_to_remove = next((item for item in order.items if item["name"] == item_name), None)
    if not item_to_remove:
        raise HTTPException(status_code=400, detail=f"Item '{item_name}' not found in order")

    order.items.remove(item_to_remove)
    recalculate_order_total(order)

    flag_modified(order, "items")
    db.commit()
    db.refresh(order)
    return {"message": f"Item '{item_name}' removed successfully", "order": order}


# Cancel Order
@router.put("/{order_id}/cancel")
async def cancel_order(order_id: UUID, db: Session = Depends(get_db)):
    """Cancel an order."""
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
    """Delete an order."""
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
