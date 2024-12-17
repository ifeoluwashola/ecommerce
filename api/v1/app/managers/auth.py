#!/usr/bin/python3

import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from typing import Optional, Dict, Any

from ....supabase.supabase_client import supabase
from ..schemas.requests.user import UpdateUser, SignInUser, UserRegister

load_dotenv()

# Construct email redirect URL
SITE_HOST = os.getenv("SITE_HOST", "localhost")
SITE_PORT = os.getenv("SITE_PORT", "8000")
EMAIL_SIGN_UP_REDIRECT_URL = f"http://{SITE_HOST}:{SITE_PORT}"


class AuthManager:
    """Manager class to handle all authentication operations."""

    @staticmethod
    def handle_supabase_request(func, *args, **kwargs) -> Any:
        """
        Centralized method to handle all Supabase requests and exceptions.
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            )

    @staticmethod
    async def create_user(user_data: Dict[str, str]) -> Any:
        """
        Registers a new user with email and password.
        :param user_data: Dictionary containing user email and password.
        :return: Supabase sign-up response.
        """
        return AuthManager.handle_supabase_request(
            supabase.auth.sign_up,
            {
                "email": user_data["email"],
                "password": user_data["password"],
                "options": {"data": user_data},
            },
        )

    @staticmethod
    async def update_user(data_to_update: UpdateUser) -> Any:
        """
        Updates a user's profile information.
        :param data_to_update: UpdateUser schema with user data to update.
        :return: Supabase user update response.
        """
        return AuthManager.handle_supabase_request(
            supabase.auth.update_user,
            {"data": data_to_update.model_dump(exclude_none=True)},
        )

    @staticmethod
    async def sign_in_user_with_passwd_and_email(user_data: Dict[str, str]) -> Any:
        """
        Signs in a user with email and password.
        :param user_data: Dictionary containing email and password.
        :return: None (raises HTTPException if authentication fails).
        """
        return AuthManager.handle_supabase_request(
            supabase.auth.sign_in_with_password,
            {"email": user_data["email"], "password": user_data["password"]},
        )

    @staticmethod
    async def sign_in_with_email_otp(email: str) -> Any:
        """
        Sends an OTP to a user's email for sign-in.
        :param email: User's registered email address.
        :return: Supabase OTP sign-in response.
        """
        return AuthManager.handle_supabase_request(
            supabase.auth.sign_in_with_otp,
            {"email": email, "options": {"email_redirect_to": EMAIL_SIGN_UP_REDIRECT_URL}},
        )

    @staticmethod
    async def sign_in_with_sms_otp(phone_number: str) -> Any:
        """
        Sends an OTP to a user's phone number for sign-in.
        :param phone_number: User's phone number.
        :return: Supabase OTP sign-in response.
        """
        return AuthManager.handle_supabase_request(
            supabase.auth.sign_in_with_otp, {"phone": phone_number}
        )

    @staticmethod
    async def sign_in_user_with_whatsapp(whatsapp_number: str) -> Any:
        """
        Signs in a user using WhatsApp OTP.
        :param whatsapp_number: User's WhatsApp-enabled phone number.
        :return: Supabase OTP sign-in response.
        """
        return AuthManager.handle_supabase_request(
            supabase.auth.sign_in_with_otp,
            {"phone": whatsapp_number, "options": {"channel": "whatsapp"}},
        )

    @staticmethod
    async def sign_in_user_with_third_party(third_party_name: str) -> Any:
        """
        Signs in a user using a third-party provider like Google, Facebook, etc.
        :param third_party_name: Third-party provider name.
        :return: Supabase OAuth sign-in response.
        """
        return AuthManager.handle_supabase_request(
            supabase.auth.sign_in_with_oauth, {"provider": third_party_name}
        )

    @staticmethod
    async def sign_out_user() -> Any:
        """
        Signs out the current user.
        :return: Supabase sign-out response.
        """
        return AuthManager.handle_supabase_request(supabase.auth.sign_out)

    @staticmethod
    async def reset_password(email: str) -> Any:
        """
        Sends a password reset email to the user.
        :param email: User's email address.
        :return: None (raises HTTPException on error).
        """
        return AuthManager.handle_supabase_request(
            supabase.auth.reset_password_for_email,
            email,
            {"redirect_to": "https://example.com/update-password"},
        )

    @staticmethod
    async def confirm_update_password(new_password: str) -> Any:
        """
        Updates a user's password.
        :param new_password: New password to set.
        :return: Supabase user update response.
        """
        return AuthManager.handle_supabase_request(
            supabase.auth.update_user, {"password": new_password}
        )
