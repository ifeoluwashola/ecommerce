#!/usr/bin/python3

import secrets
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

class Settings(BaseSettings):
    DATABASE_URL: str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_hex(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
