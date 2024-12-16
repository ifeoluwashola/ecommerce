#!/usr/bin/python3


from pydantic import BaseModel, EmailStr

from ....models.enums import RoleType


class AdminRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    photo_url: str
    role: str
    phone: str


class AdminSignIn(BaseModel):
    email: EmailStr
    password: str


class AdminUpdateProfile(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role: RoleType

