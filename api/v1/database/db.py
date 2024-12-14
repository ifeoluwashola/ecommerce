#!/usr/bin/python3


import databases
import sqlalchemy
# from decouple import config
from dotenv import load_dotenv
import os

load_dotenv()

DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# DATABASE_URL = (f"{config('DB_TYPE')}://{config('DB_USER')}:{config('DB_PASSWORD')}"
#                 f"@{config('DB_HOST')}/{config('DB_NAME')}")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
