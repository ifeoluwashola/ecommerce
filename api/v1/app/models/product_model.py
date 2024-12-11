#!/usr/bin/python3


import sqlalchemy

from ...database.db import metadata
from ..models.enums import ProductStatus


product = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("photo_url", sqlalchemy.String(250), nullable=False),
    sqlalchemy.Column("quantity", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("category", sqlalchemy.Text),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.text("timezone('UTC', now())"),
                      nullable=True),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, onupdate=sqlalchemy.text("timezone('UTC', now())"),
                      nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(ProductStatus), server_default=ProductStatus.available.name, nullable=False),
    sqlalchemy.Column("merchant_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("merchant_store_id", sqlalchemy.ForeignKey("stores.id"), nullable=False)
)

