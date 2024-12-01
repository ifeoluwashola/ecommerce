from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base

# Database URL from configuration
DATABASE_URL = settings.DATABASE_URL

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()
metadata = MetaData()