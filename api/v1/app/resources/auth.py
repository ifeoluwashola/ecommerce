from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import EmailStr, BaseModel
from sqlalchemy.orm import Session
from typing import Any
import logging
from ...database.db import get_db
from ..managers.auth import AuthManager
from ..schemas.requests.user import UserRegister, UpdateUser, SignInUser
from ...utils.auth import get_current_user

router = APIRouter(prefix="/api", tags=["User Authentication"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic Model for email input (used in sign-in OTP endpoint)
class EmailInput(BaseModel):
    email: EmailStr

@router.post("/user", status_code=status.HTTP_201_CREATED, summary="Create a new user")
async def create_user(user_details: UserRegister) -> dict:
    """
    Create a new user in Supabase Auth.
    """
    try:
        result = await AuthManager.create_user(user_details.model_dump())
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/user/update", status_code=status.HTTP_200_OK, summary="Update user profile")
async def update_user_profile(
    data: UpdateUser,
    user_id: str
) -> Any:
    """
    Update the authenticated user's profile.
    Updates data directly in `auth.users` via Supabase.
    """
    try:
        result = await AuthManager.update_user(data.model_dump(), user_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post(
    "/user/sign-in/password-email",
    status_code=status.HTTP_200_OK,
    summary="Sign in using email and password",
)
async def sign_in_user_with_password_email(user_details: SignInUser) -> Any:
    """
    Authenticate a user using email and password.
    """
    try:
        return await AuthManager.sign_in_user_with_passwd_and_email(user_details.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/user/reset-password", status_code=status.HTTP_200_OK, summary="Reset user password")
async def reset_password(email: EmailStr) -> Any:
    """
    Send a password reset email to the user.
    """
    return await AuthManager.reset_password(email)
