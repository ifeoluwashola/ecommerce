from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import EmailStr, BaseModel
from typing import Any

from ..managers.auth import AuthManager
from ..schemas.requests.user import UserRegister, UpdateUser, SignInUser


router = APIRouter(prefix="/api", tags=["User Authentication"])


# Pydantic Model for email input (used in sign-in OTP endpoint)
class EmailInput(BaseModel):
    email: EmailStr


@router.post("/user", status_code=status.HTTP_201_CREATED, summary="Create a new user")
async def create_user(user_details: UserRegister) -> Any:
    """
    Create a new user if they do not already exist.

    - **user_details**: Input from the frontend containing user registration details.
    - **Returns**: A new user object or an error message if the user already exists.
    """
    try:
        return await AuthManager.create_user(user_details.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/user/update", status_code=status.HTTP_200_OK, summary="Update user profile")
async def update_user_profile(data: UpdateUser) -> Any:
    """
    Update an existing user's profile.

    - **data**: Input from the user containing updated profile details.
    - **Returns**: Updated user object or retains original details if no changes are passed.
    """
    try:
        return await AuthManager.update_user(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/user/sign-in/password-email",
    status_code=status.HTTP_200_OK,
    summary="Sign in using password and email",
)
async def sign_in_user_with_password_email(user_details: SignInUser) -> Any:
    """
    Authenticate a user using email and password.

    - **user_details**: Input containing user's email and password.
    - **Returns**: Access token or authentication error.
    """
    try:
        return await AuthManager.sign_in_user_with_passwd_and_email(user_details.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post(
    "/user/sign-in/email-otp",
    status_code=status.HTTP_200_OK,
    summary="Sign in using email OTP",
)
async def sign_in_user_with_email_otp(email_input: EmailInput) -> Any:
    """
    Authenticate a user using an email OTP (One-Time Password).

    - **email_input**: Input containing user's email.
    - **Returns**: Access token or OTP sent notification.
    """
    try:
        return await AuthManager.sign_in_with_email_otp(email_input.email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/user/sign-in/sms-otp")
async def sign_in_user_sms_otp(phone_number: str):

    return await AuthManager.sign_in_with_sms_otp(phone_number)


@router.post("/user/sign-in/whatsapp")
async def sign_in_user_whatsapp_otp(whatsapp_number: str):

    return await AuthManager.sign_in_user_with_whatsapp(whatsapp_number)


@router.post("/user/sign-in/third-party")
async def sign_in_user_third_party(third_party: str):

    return AuthManager.sign_in_user_with_third_party(third_party)


@router.post("/user/sign-out")
async def sign_out():

    await AuthManager.sign_out_user()


@router.post("/user/reset-password")
async def reset_password(email: EmailStr):

    return await AuthManager.reset_password(email)


@router.post("/user/confirm-password-reset")
async def confirm_password_reset(new_password):

    return await AuthManager.confirm_update_password(new_password)


