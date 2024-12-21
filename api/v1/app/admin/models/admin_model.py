#!/usr/bin/python3
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ....database.db import Base
from ..models.enums import AdminType

class User(Base):
    __tablename__ = "admin_users"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    # User Info
    first_name = Column(String(50), nullable=False, comment="User's first name.")
    last_name = Column(String(50), nullable=False, comment="User's last name.")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="Unique user email address.")
    password = Column(String(128), nullable=False, comment="Hashed user password.")
    location = Column(String(100), nullable=False, comment="User's location.")
    
    # Optional Fields
    photo_url = Column(String(250), nullable=True, comment="Optional photo URL for the user.")
    phone = Column(String(20), nullable=True, comment="Optional phone number.")
    
    # Role and Status
    role = Column(Enum(AdminType), default=AdminType.regular_admin, nullable=False, comment="User role. Default is 'buyer'.")
   
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, comment="Soft delete timestamp.")
