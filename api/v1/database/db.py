#!/usr/bin/python3

import os
import databases
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
from ..utils.config import settings
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = settings.DATABASE_URL

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()
metadata = MetaData()