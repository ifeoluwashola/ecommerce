from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Product, Category
from database import get_db
from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import List, Optional

router = APIRouter()

NOTFOUND = "Product not found"

# Pydantic schemas
class NewCategory(BaseModel):
    name: str = Field(..., example="string")
    description: Optional[str] = Field(None, example="string")

    @validator("name")
    def validate_name(cls, name):
        if not name.strip():
            raise ValueError("Category name cannot be empty.")
        return name

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[UUID] = None  # Existing category
    new_category: Optional[NewCategory] = None  # Create new category if not exists
    stock: int
    currency: str = "USD"  # Default currency

class ProductRead(ProductCreate):
    product_id: UUID

class StockUpdate(BaseModel):
    quantity: int

# Create a new product
@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product with optional new category."""
    # Handle new category creation
    if product.new_category:
        # Convert new_category to dictionary before passing to Category constructor
        new_category = Category(**product.new_category.dict())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        product.category_id = new_category.category_id

    if not product.category_id:
        raise HTTPException(
            status_code=400, detail="A valid category_id or new_category is required."
        )

    # Create product
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
        stock=product.stock,
        currency=product.currency,  # Store the currency
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Create multiple products in bulk
@router.post("/bulk", response_model=List[ProductRead])
def create_products_bulk(products: List[ProductCreate], db: Session = Depends(get_db)):
    """Create multiple products in bulk with optional categories."""
    db_products = []
    for product in products:
        # Handle new category
        if product.new_category:
            existing_category = db.query(Category).filter(Category.name == product.new_category.name).first()
            if existing_category:
                # Use existing category
                product.category_id = existing_category.category_id
            else:
                # Create new category
                new_category = Category(**product.new_category.dict())
                db.add(new_category)
                db.commit()
                db.refresh(new_category)
                product.category_id = new_category.category_id

        if not product.category_id:
            raise HTTPException(
                status_code=400, detail="A valid category_id or new_category is required."
            )

        # Add product
        db_products.append(
            Product(
                name=product.name,
                description=product.description,
                price=product.price,
                category_id=product.category_id,
                stock=product.stock,
                currency=product.currency,
            )
        )

    db.add_all(db_products)
    db.commit()
    return db.query(Product).filter(
        Product.product_id.in_([p.product_id for p in db_products])
    ).all()

# Get product by ID
@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    """Retrieve a product by ID."""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    return product

# List all products
@router.get("/", response_model=List[ProductRead])
def list_products(
    category_id: Optional[UUID] = None, db: Session = Depends(get_db)
):
    """List all products with optional category filtering."""
    query = db.query(Product).filter(Product.stock > 0)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.all()

# Update a product
@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: UUID, product: ProductCreate, db: Session = Depends(get_db)):
    """Update product details."""
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail=NOTFOUND)

    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

# Add stock to a product
@router.patch("/{product_id}/stock/add")
def add_stock(product_id: UUID, stock_update: StockUpdate, db: Session = Depends(get_db)):
    """Add stock to a product."""
    if stock_update.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity to add must be greater than zero")

    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=NOTFOUND)

    product.stock += stock_update.quantity
    db.commit()
    db.refresh(product)
    return {"message": "Stock added successfully", "product": product}

# Remove stock from a product
@router.patch("/{product_id}/stock/remove")
def remove_stock(product_id: UUID, stock_update: StockUpdate, db: Session = Depends(get_db)):
    """Remove stock from a product."""
    if stock_update.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity to remove must be greater than zero")

    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=NOTFOUND)

    if product.stock < stock_update.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock available")

    product.stock -= stock_update.quantity
    db.commit()
    db.refresh(product)
    return {"message": "Stock removed successfully", "product": product}

# Delete a product
@router.delete("/{product_id}")
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    """Delete a product by ID."""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
