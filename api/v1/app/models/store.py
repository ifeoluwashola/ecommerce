import sqlalchemy

from ...database.db import metadata
from ..models.enums import StoreStatus


store = sqlalchemy.Table(
    "stores",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("photo_url", sqlalchemy.String(250), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("speciality", sqlalchemy.Text),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.text("timezone('UTC', now())"),
                      nullable=True),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, onupdate=sqlalchemy.text("timezone('UTC', now())"),
                      nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(StoreStatus), server_default=StoreStatus.inactive.name, nullable=False),
    sqlalchemy.Column("owner_id", sqlalchemy.ForeignKey("users.id"), nullable=False)
)

