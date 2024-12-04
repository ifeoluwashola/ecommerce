from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from decimal import Decimal


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    category: Optional[str] = Field(None, max_length=100)
    images: Optional[List[str]] = []


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=100)
    images: Optional[List[str]] = None


class ProductRead(ProductBase):
    id: UUID
    seller_id: UUID
    is_active: bool

    class Config:
        from_attribute = True
