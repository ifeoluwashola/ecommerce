#!/usr/bin/python3

from ....supabase.supabase_client import supabase


class UserManager:
    """This class is going to handle all user related logic"""
    @staticmethod
    async def get_all_user():
        """
        This method queries the database through supabase to get all users from the database:
        :returns - list of users
        """
        result = supabase.table("users").select("*").execute()
        return result
