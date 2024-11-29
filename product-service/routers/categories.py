from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Category, Product
from database import get_db
from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

router = APIRouter()
NOTFOUND = "Category not found"
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    category_id: UUID

@router.post("/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    """List all categories."""
    return db.query(Category).all()

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    """Retrieve a category by ID."""
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    return category

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: UUID, category: CategoryBase, db: Session = Depends(get_db)):
    """Update a category."""
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    db_category.name = category.name
    db_category.description = category.description
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/categories/dropdown", response_model=List[CategoryRead])
def get_categories_dropdown(db: Session = Depends(get_db)):
    """Get all categories for dropdown selection."""
    return db.query(Category).all()

@router.delete("/{category_id}")
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    """Delete a category."""
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}
