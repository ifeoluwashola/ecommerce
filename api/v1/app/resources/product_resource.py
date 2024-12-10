from typing import List

from fastapi import APIRouter, status

from ..managers.product_manager import ProductManager
from ..schemas.resquests.product import ProductRead

router = APIRouter()


@router.get("/products", response_model=List[ProductRead])
async def list_products():
    """
    List products with pagination, filtering, and search.
    """
    return await ProductManager.list_products()


@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product(product_id):
    """Get details of a single product."""
    return await ProductManager.get_product(product_id)


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product_data):
    """Create a new product (Seller only)."""
    return ProductManager.create_product(product_data)


@router.put("/products/{product_id}", response_model=ProductRead)
async def update_product(product_id, product_data):
    """Update product details (Seller only)."""
    return await ProductManager.update_product(product_id, product_data)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id):
    """Delete a product (Seller only)."""
    return await ProductManager.delete_product(product_id)

