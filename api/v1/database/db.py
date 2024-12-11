#!/usr/bin/python3


import databases
import sqlalchemy
from decouple import config

DATABASE_URL = (f"{config('DB_TYPE')}://{config('DB_USER')}:{config('DB_PASSWORD')}"
                f"@{config('DB_HOST')}/{config('DB_NAME')}")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
