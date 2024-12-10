from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Column, Float, JSON, Enum
from ...database.db import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum


class OrderStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    items = Column(MutableList.as_mutable(JSON), nullable=False)  # List of items with prices
    total_price = Column(Float, nullable=False, default=0.0)  # Automatically calculated
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
