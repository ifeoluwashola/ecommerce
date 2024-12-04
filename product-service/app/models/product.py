import uuid
from sqlalchemy import Column, String, Boolean, Numeric, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)  # Example: 999.99
    quantity = Column(Integer, nullable=False)
    seller_id = Column(UUID(as_uuid=True), nullable=False)  # Foreign key to seller (not enforced in model)
    category = Column(String, nullable=True)
    images = Column(JSON, default=[])  # Store image URLs as JSON array
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
