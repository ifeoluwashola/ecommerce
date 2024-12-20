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
    async def get_and_update_user(user_id: str, data_to_update: dict = None) -> dict:
        """
        Fetches current user data and optionally updates their profile in Supabase Auth.
        If `data_to_update` is None, returns the current user data. If fields in `data_to_update`
        are missing or empty, retains the current values.
        """
        try:
            # Fetch current user data
            current_user = supabase.auth.get_user()
            if not current_user:
                raise HTTPException(status_code=404, detail="User not found.")
    
            # Extract current data
            current_data = {
                "email": current_user.user.email,
                "first_name": current_user.user.user_metadata.get("first_name", ""),
                "last_name": current_user.user.user_metadata.get("last_name", ""),
                "location": current_user.user.user_metadata.get("location", ""),
                "photo_url": current_user.user.user_metadata.get("photo_url", ""),
                "phone": current_user.user.user_metadata.get("phone", ""),
                "role": current_user.user.user_metadata.get("role", None),
            }
    
            # If no update data is provided, return the current user data
            if data_to_update is None:
                return current_data
    
            # Merge current data with the update data, preserving existing values
            updated_data = {
                key: data_to_update.get(key) if data_to_update.get(key) not in [None, ""] else value
                for key, value in current_data.items()
            }
    
            # Proceed to update user data
            response = supabase.auth.update_user({
                "email": updated_data["email"],
                "data": {
                    "first_name": updated_data["first_name"],
                    "last_name": updated_data["last_name"],
                    "location": updated_data["location"],
                    "photo_url": updated_data["photo_url"],
                    "phone": updated_data["phone"],
                    "role": updated_data["role"],
                }
            })
    
            if not response.user:
                raise HTTPException(status_code=400, detail="Failed to update user in Supabase Auth.")
    
            return {
                "message": "User updated successfully",
                "user_id": response.user.email
            }
        except Exception as e:
            logger.error(f"Error in get_and_update_user: {str(e)}")
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
