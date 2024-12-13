from fastapi import APIRouter
from pydantic import EmailStr

from ..managers.auth import AuthManager
from ..schemas.resquests.user import UserRegister, UpdateUser, SignInUser


router = APIRouter(prefix="/auth", tags=["User Authentication"])


@router.post("/user")
async def create_user(user_details: UserRegister):
    """
    This endpoint will create a user if it does not already in existence:
    :param user_details: this user input from the frontend.
    :return: a new user object if the user does not already exist or 'User already exists' response
    """
    return await AuthManager.create_user(user_details)


@router.patch("/user/update")
async def update_user_profile(data: UpdateUser):
    """
    This handles any update by the user to their profile
    :param data: inputs from the user passed to the backend from the frontend.
    :return: updated user object if any valid inputs are passed or retains the details unchanged if nothing is passed.
    """
    return await AuthManager.update_user(data)


@router.post("/user/sign_in/passwd_email")
async def sign_in_user_password_email(user_details: SignInUser):

    return await AuthManager.sign_in_user_with_passwd_and_email(user_details)


@router.post("/user/sign_in/email_otp")
async def sign_in_user_email_otp(email: EmailStr):

    return await AuthManager.sign_in_with_email_otp(email)


@router.post("/user/sign_in/sms_otp")
async def sign_in_user_sms_otp(phone_number: str):

    return await AuthManager.sign_in_with_sms_otp(phone_number)


@router.post("/user/sign_in/whatsapp")
async def sign_in_user_whatsapp_otp(whatsapp_number: str):

    return await AuthManager.sign_in_user_with_whatsapp(whatsapp_number)


@router.post("/user/sign_in/third_party")
async def sign_in_user_third_party(third_party: str):

    return AuthManager.sign_in_user_with_third_party(third_party)


@router.post("/user/sign_out")
async def sign_out():

    await AuthManager.sign_out_user()


@router.post("/user/reset_password")
async def reset_password(email: EmailStr):

    return await AuthManager.reset_password(email)


@router.post("/user/confirm_password_reset")
async def confirm_password_reset(new_password):

    return await AuthManager.confirm_update_password(new_password)


