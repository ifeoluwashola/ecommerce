#!/usr/bin/python3


import sqlalchemy

from ....database.db import metadata
from ..models.enums import AdminType

user = sqlalchemy.Table(
    "admins",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String(250), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(100), nullable=False, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("role", sqlalchemy.Enum(AdminType), server_default=AdminType.regular_admin.name, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.text("timezone('UTC', now())"),
                      nullable=True),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime, server_default=sqlalchemy.text("timezone('UTC', now())"),
                      nullable=True),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, onupdate=sqlalchemy.text("timezone('UTC', now())"),
                      nullable=True)
)
