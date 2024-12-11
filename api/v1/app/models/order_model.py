#!/usr/bin/python3


import sqlalchemy

from ...database.db import metadata
from ..models.enums import OrderStatus


order = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("description", sqlalchemy.Text),
    # sqlalchemy.Column("photo_url", sqlalchemy.String(250), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.text("timezone('UTC', now())"), nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(OrderStatus), server_default=OrderStatus.pending.name, nullable=True),
    sqlalchemy.Column("buyer_id", sqlalchemy.ForeignKey("users.id"), nullable=False)
)

