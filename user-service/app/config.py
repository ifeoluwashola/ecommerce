import os
import secrets
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/users_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_hex(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SMTP_HOST: str = os.getenv("SMTP_HOST", "sandbox.smtp.mailtrap.io")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "544c39a2751e84")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "b3065d69620be8")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()