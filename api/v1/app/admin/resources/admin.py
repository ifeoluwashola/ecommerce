from fastapi import APIRouter
from pydantic import EmailStr

from ..schemas.requests.admin import AdminRegister, AdminSignIn, AdminUpdateProfile


from ..managers.auth import AdminAuthManager


router = APIRouter(prefix="/admin/auth", tags=["Admin Endpoints"])


@router.post("/user")
async def create_user(user_data: AdminRegister):

    return await AdminAuthManager.create_user(user_data.model_dump())


@router.put("/user/{user_id}")
async def update_user(user_id: str, user_data_to_update: AdminUpdateProfile):
    print(user_data_to_update.dict())

    return await AdminAuthManager.update_a_user_by_id(user_id, user_data_to_update)


@router.delete("/user/{user_id}")
async def delete_user(user_id):

    return await AdminAuthManager.delete_user(user_id)


@router.post("/user/invite")
async def invite_user(email: EmailStr):

    return await AdminAuthManager.invite_a_user(email)


@router.get("/user/{user_id}")
async def get_user_by_id(user_id: str):

    return await AdminAuthManager.get_user_by_id(_id=user_id)


@router.get("/users")
async def get_all_users():

    return await AdminAuthManager.get_all_users()


