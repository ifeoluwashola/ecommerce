import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from ....supabase.supabase_client import supabase
from ..schemas.requests.user import UpdateUser
import logging

# Load environment variables
load_dotenv()

# Properly format email redirect URL
EMAIL_SIGN_UP_REDIRECT_URL = f"{os.getenv('SITE_HOST')}:{os.getenv('SITE_PORT')}"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    @staticmethod
    async def _handle_request(method_name, *args, **kwargs):
        """Helper method to handle requests and exceptions."""
        try:
            method = getattr(supabase.auth, method_name)
            response = method(*args, **kwargs)

            # Convert response to dictionary for JSON serialization
            if hasattr(response, "user") or hasattr(response, "session"):
                response_dict = {
                    "user": response.user.__dict__ if response.user else None,
                    "session": response.session.__dict__ if response.session else None
                }
                logger.info(f"AuthManager.{method_name} successful.")
                return response_dict
        
            # If response is already a dict or primitive, return as is
            return response

        except Exception as e:
            logger.error(f"AuthManager.{method_name} failed: {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    async def create_user(user_data):
        return await AuthManager._handle_request("sign_up", {
            "email": user_data["email"],
            "password": user_data["password"],
            "options": {"data": user_data},
        })
    
    @staticmethod
    async def update_user(data_to_update: UpdateUser):
        return await AuthManager._handle_request("update_user", {
            "data": data_to_update.model_dump()
        })

    @staticmethod
    async def sign_in_user_with_passwd_and_email(user_data):
        return await AuthManager._handle_request("sign_in_with_password", {
            "email": user_data["email"],
            "password": user_data["password"]
        })

    @staticmethod
    async def sign_in_with_email_otp(email):
        return await AuthManager._handle_request("sign_in_with_otp", {
            "email": email,
            "options": {"email_redirect_to": EMAIL_SIGN_UP_REDIRECT_URL},
        })

    @staticmethod
    async def sign_in_with_sms_otp(phone_number):
        return await AuthManager._handle_request("sign_in_with_otp", {
            "phone": phone_number,
        })

    @staticmethod
    async def sign_in_user_with_whatsapp(whatsapp_number):
        return await AuthManager._handle_request("sign_in_with_otp", {
            "phone": whatsapp_number,
            "options": {"channel": "whatsapp"}
        })

    @staticmethod
    async def sign_in_user_with_third_party(provider_name):
        return await AuthManager._handle_request("sign_in_with_oauth", {
            "provider": provider_name
        })

    @staticmethod
    async def sign_out_user():
        return await AuthManager._handle_request("sign_out")

    @staticmethod
    async def reset_password(email):
        return await AuthManager._handle_request("reset_password_for_email", email, {
            "redirect_to": "https://example.com/update-password",
        })

    @staticmethod
    async def confirm_update_password(new_password):
        return await AuthManager._handle_request("update_user", {
            "password": new_password
        })
