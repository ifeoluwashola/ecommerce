#!/usr/bin/python3


from pydantic import BaseModel, EmailStr


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
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    phone: str = None
