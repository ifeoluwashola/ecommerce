#!/usr/bin/python3


from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    cancel = "canceled"


class RoleType(str, Enum):
    merchant = "merchant"
    buyer = "buyer"
    admin = "admin"


class ProductStatus(str, Enum):
    available = "available"
    unavailable = "unavailable"
    limited = "limited"


class StoreStatus(str, Enum):
    active = "active"
    inactive = "inactive"
