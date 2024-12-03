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
    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)

class AdminCreate(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=8, max_length=128)