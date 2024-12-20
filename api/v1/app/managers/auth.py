import os
from fastapi import HTTPException, status
from ....supabase.supabase_client import supabase, service_client
import logging
import bcrypt

# Load environment variables
EMAIL_SIGN_UP_REDIRECT_URL = f"{os.getenv('SITE_HOST')}:{os.getenv('SITE_PORT')}"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    @staticmethod
    async def _handle_request(method_name, *args, **kwargs):
        """
        Helper method to handle Supabase Auth requests.
        """
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
    async def create_user(user_data: dict) -> dict:
        """
        Creates a new user in Supabase Auth.
        """
        try:
            auth_table = supabase.auth.sign_up({
                "email": user_data["email"],
                "password": user_data["hashed_password"],
                "phone": user_data["phone"],
                "options": {
                    "data": {
                        "first_name": user_data.get("first_name"),
                        "last_name": user_data.get("last_name"),
                        "location": user_data.get("location"),
                        "photo_url": user_data.get("photo_url"),
                        "phone": user_data.get("phone"),
                        "role": user_data.get("role", "buyer")
                    }
                }
            })

            hashed_password = bcrypt.hashpw(user_data["hashed_password"].encode(), bcrypt.gensalt()).decode()
            public_table = (service_client.table("users")
                            .insert({
                                **user_data,
                                "id": auth_table.user.id,
                                "is_active": True,
                                "hashed_password": hashed_password
                            })
                            .execute())
            
            if not auth_table.user:
                raise HTTPException(status_code=400, detail="Failed to create user in Supabase Auth.")

            
            return {
                "message": "User created successfully",
                "user_id": auth_table.user.user_metadata
            }
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @staticmethod
    async def fetch_user(user_id: str) -> dict:
        """
        Fetch a user's profile using the Supabase client.
        """
        try:
            # Retrieve user from Supabase Auth
            user_response = supabase.auth.get_user()

            if not user_response or user_response.user.id != user_id:
                raise HTTPException(status_code=404, detail="User not found.")

            # Return user metadata
            return user_response.user.user_metadata
        except Exception as e:
            logger.error(f"Error fetching user: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @staticmethod
    async def update_user(data_to_update: dict, user_id: str) -> dict:
        """
        Updates a user's profile in Supabase Auth.
        """
        try:
            response = supabase.auth.update_user({
                "email": data_to_update.get("email"),
                "data": {
                    "first_name": data_to_update.get("first_name"),
                    "last_name": data_to_update.get("last_name"),
                    "location": data_to_update.get("location"),
                    "photo_url": data_to_update.get("photo_url"),
                    "phone": data_to_update.get("phone"),
                    "role": data_to_update.get("role")
                }
            })

            if not response.user:
                raise HTTPException(status_code=400, detail="Failed to update user in Supabase Auth.")

            return {
                "message": "User updated successfully",
                "user_id": response.user.id
            }
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
            
    @staticmethod
    async def sign_in_user_with_passwd_and_email(user_data: dict) -> dict:
        """
        Signs in a user with email and password.
        """
        return await AuthManager._handle_request("sign_in_with_password", {
            "email": user_data["email"],
            "password": user_data["hashed_password"]
        })

    @staticmethod
    async def reset_password(email: str) -> dict:
        """
        Sends a password reset email to the user.
        """
        return await AuthManager._handle_request("reset_password_for_email", email, {
            "redirect_to": EMAIL_SIGN_UP_REDIRECT_URL
        })
