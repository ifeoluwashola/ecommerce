from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.db.session import SessionLocal
from app.utils.auth import get_current_user, require_role
from typing import List
from uuid import UUID

router = APIRouter()
NOT_FOUND = "Product not found."

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products", response_model=List[ProductRead])
def list_products(
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

@router.get("/products/{id}", response_model=ProductRead)
def get_product(id: UUID, db: Session = Depends(get_db)):
    """
    Get details of a single product.
    """
    product = db.query(Product).filter(Product.id == id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return product


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
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


@router.put("/products/{id}", response_model=ProductRead)
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)

    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully."}
