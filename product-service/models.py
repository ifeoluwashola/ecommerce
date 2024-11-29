from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    # Relationship with products
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"), nullable=True)
    stock = Column(Integer, default=0)
    currency = Column(String, nullable=False, default="USD")  # New field for currency
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with category
    category = relationship("Category", back_populates="products")
