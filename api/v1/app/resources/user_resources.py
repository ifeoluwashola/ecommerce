#!/usr/bin/python3


from fastapi import APIRouter

from ..managers.user_manager import UserManager


router = APIRouter(prefix="/user", tags=["User Related Endpoints"])


@router.get("/user/me")
async def get_user_profile():

    return await UserManager.get_user_profile()



