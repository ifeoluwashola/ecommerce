#!/usr/bin/python3


import datetime
from typing import Optional

import jwt
from decouple import config
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from ...database.db import database
from ..models.user_model import User
from ..models.enums import RoleType


class AuthManager:

    @staticmethod
    def encode_token(user_data):
        try:
            payload = {
                "id": user_data["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
            }
            return jwt.encode(payload=payload, key=config("JWT_SECRET_KEY"), algorithm="HS256")
        except Exception as ex:
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            token = jwt.decode(res.credentials, config("JWT_SECRET_KEY"), algorithms=["HS256"])
            user_id = token["id"]
            if not user_id:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Not Found")
            user_data_from_db = await database.fetch_one(User.select().where(User.c.id == user_id))
            request.state.user = user_data_from_db
            return user_data_from_db
        except jwt.InvalidSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Expired signature")
        except jwt.InvalidTokenError as ex:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"{ex}")


oauth2_schema = CustomHTTPBearer()


def is_merchant(request: Request):
    if not request.state.user["role"] == RoleType.merchant:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this operation")


def is_seller(request: Request):
    if not request.state.user["role"] == RoleType.seller:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this operation")


def is_admin(request: Request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this operation")

