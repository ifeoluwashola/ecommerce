from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid

# Shared properties for User
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=15)

# Properties for user creation (registration)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    role: Optional[str] = Field(default="buyer", pattern="^(buyer|seller)$")

# Properties for reading a user's profile
class UserRead(UserBase):
    id: uuid.UUID
    role: str
    avatar_url: Optional[str]

    class Config:
        from_attributes = True  # Allows SQLAlchemy models to be used as data sources
