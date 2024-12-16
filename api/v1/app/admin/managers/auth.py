#!/usr/bin/python3

from fastapi import HTTPException, status

from .....supabase.supabase_admin import admin_auth_client
from ..schemas.requests.admin import AdminRegister, AdminSignIn, AdminUpdateProfile


class AdminAuthManager:

    @staticmethod
    async def create_user(user_data):
        """
        This function is going to register a new admin
        :param user_data:
        :return a user object after a successful registration:
        """
        try:
            response = admin_auth_client.create_user(
                {
                    "email": user_data["email"],
                    "password": user_data["password"],
                    "user_metadata": {"first_name": user_data["first_name"],
                                      "last_name": user_data["last_name"],
                                      "role": user_data["role"],
                                      "phone": user_data["phone"]
                                      }
                }
            )
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def get_user_by_id(_id):
        """
        This will help get a user with the provided is
        :param _id:
        :return:
        """
        try:

            response = admin_auth_client.get_user_by_id(_id)

            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def get_all_users():
        """
        This will help get the list of users from the database
        :return a list of users:
        """
        try:
            response = admin_auth_client.list_users()

            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def delete_user(user_id):
        """
        This will help delete user from the database
        :param user_id:
        :return:
        """
        try:
            response = admin_auth_client.delete_user(user_id, should_soft_delete=True)
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def invite_a_user(user_email):
        """
        This will allow an admin to invite people to register on the platform via thier email
        :param user_email:
        :return:
        """
        try:
            response = admin_auth_client.invite_user_by_email(user_email)

            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def update_a_user_by_id(_id, user_data: AdminUpdateProfile):

        """
        This will allow an admin to update user's details
        :param _id:
        :param user_data:
        :return:
        """
        print(user_data.dict())
        try:
            response = admin_auth_client.update_user_by_id(
                _id,
                {"user_metadata": user_data.dict()}
            )

            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

