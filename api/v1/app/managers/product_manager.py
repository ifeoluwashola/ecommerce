from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..models.product_model import Product
from ..schemas.resquests.product import ProductCreate, ProductRead, ProductUpdate
from ..schemas.responses.custom_responses import PRODUCT_NOT_FOUND
from ...database.db import SessionLocal, get_db
from ...utils.auth import get_current_user, require_role
from uuid import UUID


class ProductManager:
    """This manages all the Product related logic and database transactions"""

    @staticmethod
    async def list_products(
            db: Session = Depends(get_db),
            skip: int = Query(0, ge=0),
            limit: int = Query(10, ge=1, le=100),
            search: str = Query(None),
            category: str = Query(None),
    ):
        """
        List products with pagination, filtering, and search.
        """
        query = db.query(Product).filter(Product.is_active == True)

        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))
        if category:
            query = query.filter(Product.category == category)

        products = query.offset(skip).limit(limit).all()
        return products

    @staticmethod
    async def get_product(id: UUID, db: Session = Depends(get_db)):
        """
        Get details of a single product.
        """
        product = db.query(Product).filter(Product.id == id, Product.is_active == True).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PRODUCT_NOT_FOUND)
        return product

    @staticmethod
    async def create_product(
            product: ProductCreate,
            current_user=Depends(require_role("seller")),
            db: Session = Depends(get_db),
    ):
        """
        Create a new product (Seller only).
        """
        new_product = Product(**product.model_dump(), seller_id=current_user["user_id"])
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    @staticmethod
    def update_product(
            id: UUID,
            product_update: ProductUpdate,
            current_user=Depends(require_role("seller")),
            db: Session = Depends(get_db),
    ):
        """
        Update product details (Seller only).
        """
        product = db.query(Product).filter(Product.id == id, Product.seller_id == current_user.id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PRODUCT_NOT_FOUND)

        for key, value in product_update.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(
            id: UUID,
            current_user=Depends(require_role("seller")),
            db: Session = Depends(get_db),
    ):
        """
        Delete a product (Seller only).
        """
        product = db.query(Product).filter(Product.id == id, Product.seller_id == current_user.id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PRODUCT_NOT_FOUND)

        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully."}

