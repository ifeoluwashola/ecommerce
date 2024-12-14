#!/usr/bin/python3

# from decouple import config
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status

from ....supabase.supabase_client import supabase
from ..schemas.resquests.user import UpdateUser, SignInUser, UserRegister
from ..schemas.responses.custom_responses import UNEXPECTED_ERROR

load_dotenv()
EMAIL_SIGN_UP_REDIRECT_URL = f"{os.getenv('SITE_HOST'), os.getenv('SITE_PORT')}"


class AuthManager:
    @staticmethod
    async def create_user(user_data):
        """Registers a user and returns the response or error."""
        try:
            response = supabase.auth.sign_up(
                {
                    "email": user_data["email"],
                    "password": user_data["password"],
                    "options": {
                        "data": user_data
                    }
                }
            )
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        # I am putting this here incase we need to redirect our users to a special page after they are just registered.
        # 'options': {
        #     'email_redirect_to': EMAIL_SIGN_UP_REDIRECT_URL,
        # }

    @staticmethod
    async def update_user(data_to_update: UpdateUser):
        """
        This function handles user profile update
        :param data_to_update:
        :return: A user object as user profile
        """
        try:
            response = supabase.auth.update_user({
                "data": data_to_update.dict()
            })
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def sign_in_user_with_passwd_and_email(user_data):
        """
        This function sings in a user provided the user has the correct credentials, such as email and password
        :param user_data: the user's details
        :return: it signs in a user if the credentials are correct.
        """
        try:
            supabase.auth.sign_in_with_password(
                {
                    "email": user_data["email"],
                    "password": user_data["password"]
                }
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def sign_in_with_email_otp(email):
        """
        This will help sign in user with their registered email.
        :param email:
        :return:
        """
        try:
            response = supabase.auth.sign_in_with_otp(
                {
                    "email": email,
                    "options": {"email_redirect_to": EMAIL_SIGN_UP_REDIRECT_URL},
                }
            )
            return response

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def sign_in_with_sms_otp(phone_number):
        """
        This will sign in user with their phone number.
        :param phone_number:
        :return:
        """
        try:

            response = supabase.auth.sign_in_with_otp({
                "phone": phone_number,
            })
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def sign_in_user_with_whatsapp(whatsapp_number):
        """
        This will sign in user with their WhatsApp number.
        :param whatsapp_number:
        :return:
        """
        try:
            response = supabase.auth.sign_in_with_otp({
                "phone": whatsapp_number,
                "options": {
                    "channel": "whatsapp",
                }
            })
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def sign_in_user_with_third_party(third_party_name):
        """
        This will sign in user with third-party app such as Google, Facebook etc.
        :param third_party_name:
        :return:
        """
        try:

            response = supabase.auth.sign_in_with_oauth({
                "provider": third_party_name
            })
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def sign_out_user():
        """
        This function will sign out user from the app
        :return:
        """
        try:

            response = supabase.auth.sign_out()

            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def reset_password(email):
        """
        This will take a user's email and sends a link to the email for the user to reset their password.
        :param email:
        :return:
        """
        try:
            supabase.auth.reset_password_for_email(email, {
                "redirect_to": "https://example.com/update-password",
            })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def confirm_update_password(new_password):
        """
        This will make the user input their desired new password.
        :param new_password:
        :return:
        """
        try:
            response = supabase.auth.update_user({
                "password": new_password
            })
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

