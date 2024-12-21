#!/usr/bin/python3

from string import punctuation
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, Field
from ...models.enums import RoleType


# Shared Password Validator
def validate_password(hashed_password: str) -> str:
    """Validates password strength."""
    if not any(c.isupper() for c in hashed_password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in hashed_password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in hashed_password):
        raise ValueError("Password must contain at least one digit.")
    if not any(c in punctuation for c in hashed_password):
        raise ValueError("Password must contain at least one special character.")
    return hashed_password


# User Registration Schema
class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="User's email address.")
    hashed_password: str = Field(..., min_length=8, max_length=128, description="Password must be strong.")
    first_name: str = Field(..., description="User's first name.")
    last_name: str = Field(..., description="User's last name.")
    location: str = Field(..., description="User's location.")
    phone: Optional[str] = Field(None, description="Optional phone number.")
    role: str = Field(default=RoleType.buyer.name, description="User role. Defaults to 'buyer'.")

    @field_validator("hashed_password")
    def validate_password_strength(cls, value):
        return validate_password(value)


# Update User Schema
class UpdateUser(BaseModel):
    email: Optional[EmailStr] = Field(None, description="User's updated email address.")
    first_name: Optional[str] = Field(None, description="User's updated first name.")
    last_name: Optional[str] = Field(None, description="User's updated last name.")
    photo_url: Optional[str] = Field(None, description="Updated photo URL.")
    phone: Optional[str] = Field(None, description="Updated phone number.")
    location: Optional[str] = Field(None, description="Updated location.")

# Sign In Schema
class SignInUser(BaseModel):
    email: EmailStr = Field(..., description="User's email for sign-in.")
    hashed_password: str = Field(..., description="User's password for sign-in.")
