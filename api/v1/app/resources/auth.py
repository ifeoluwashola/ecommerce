from fastapi import APIRouter, HTTPException, status, Request
from pydantic import EmailStr, BaseModel
from typing import Any
import logging
from ..managers.auth import AuthManager
from ..schemas.requests.user import UserRegister, SignInUser
from ....supabase.supabase_client import supabase

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

@router.patch("/user/update", status_code=status.HTTP_200_OK, summary="Fetch or update user profile")
async def update_user_profile(
    user_id: str,
    request: Request
) -> Any:
    """
    Fetch or update the authenticated user's profile.
    - Fetches current user data when called without a body.
    - Updates user data when a body with modified fields is provided.
    """
    try:
        # Try to read the request body, fallback to None if empty
        try:
            update_data = await request.json()
        except Exception:
            update_data = None  # No data provided in the request

        # Pass the data to the service for fetching/updating
        result = await AuthManager.get_and_update_user(user_id=user_id, data_to_update=update_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

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
