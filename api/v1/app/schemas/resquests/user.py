#!/usr/bin/python3

from string import punctuation

from pydantic import BaseModel, EmailStr, field_validator, Field

from ...models.enums import RoleType


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, description="Password must be strong.")
    first_name: str
    last_name: str
    photo_url: str = None
    phone: str = None
    role: str = RoleType.buyer.name

    @classmethod
    def check_password(cls, value):
        # Ensure the value is a string
        value = str(value)

        # Define validation criteria
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(c in punctuation for c in value):
            raise ValueError("Password must contain at least one special character.")

        return value


class UpdateUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    photo_url: str
    phone: str


class SignInUser(BaseModel):
    email: EmailStr
    password: str


