#!/usr/bin/python3


import secrets
from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = config("DATABASE_URL")
    SECRET_KEY: str = config("SECRET_KEY", secrets.token_hex(32))
    ALGORITHM: str = config("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
