#!/usr/bin/python3

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from string import punctuation
from ...models.enums import RoleType


# Shared Password Validator
def validate_password(password: str) -> str:
    """Validates password strength."""
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit.")
    if not any(c in punctuation for c in password):
        raise ValueError("Password must contain at least one special character.")
    return password


# User Registration Schema
class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="User's email address.")
    password: str = Field(..., min_length=8, max_length=128, description="Password must be strong.")
    first_name: str = Field(..., description="User's first name.")
    last_name: str = Field(..., description="User's last name.")
    location: str = Field(..., description="User's location.")
    photo_url: Optional[str] = Field(None, description="Optional photo URL for the user.")
    phone: Optional[str] = Field(None, description="Optional phone number.")
    role: str = Field(default=RoleType.buyer.name, description="User role. Defaults to 'buyer'.")

    @field_validator("password")
    def validate_password_strength(cls, value):
        return validate_password(value)


# Update User Schema
class UpdateUser(BaseModel):
    email: EmailStr = Field(..., description="User's updated email address.")
    first_name: str = Field(..., description="User's updated first name.")
    last_name: str = Field(..., description="User's updated last name.")
    photo_url: Optional[str] = Field(None, description="Updated photo URL.")
    phone: Optional[str] = Field(None, description="Updated phone number.")
    location: Optional[str] = Field(None, description="Updated location.")


# Sign In Schema
class SignInUser(BaseModel):
    email: EmailStr = Field(..., description="User's email for sign-in.")
    password: str = Field(..., description="User's password for sign-in.")
