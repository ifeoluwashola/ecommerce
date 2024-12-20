import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Replace with your Supabase project URL
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Replace with your Supabase API Key
HEADRES = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
# FastAPI Configuration
BASE_URL = "http://localhost:8000"
UPDATE_ENDPOINT = "/api/user/update"

# User Login Credentials
LOGIN_CREDENTIALS = {
    "email": "ifeoluwadlove@gmail.com",  # Replace with user's email
    "password": "Ifeoluwa.1"  # Replace with user's password
}

# Headers for Supabase Auth Request
supabase_headers = HEADRES

def sign_in_user():
    """
    Logs in the user via Supabase and retrieves the JWT token.
    """
    login_url = "http://localhost:8000/api/user/sign-in/password-email"
    response = requests.post(login_url, headers=supabase_headers, json=LOGIN_CREDENTIALS)

    if response.status_code == 200:
        print("User signed in successfully!")
        jwt_token = response.json().get("access_token")
        # print("JWT Token", jwt_token)
        return jwt_token
    else:
        print(f"Failed to sign in: {response.status_code}")
        print("Response:", response.json())
        return None

def get_user_profile():
    headers = HEADRES
    try:
        response = requests.get('http://localhost:8000/user/user/me', headers=headers)
        if response.status_code == 200:
            print("User Data")
            print("User data:", response.json())
        else:
            print(f"Failed to get user data: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"Error occured: {str(e)}")

def update_user_profile():
    """
    Updates the user's profile using the JWT token for authentication.
    """
    # Headers with JWT Token
    headers = HEADRES

    # Data to Update
    data = {
        "first_name": "Jane",
        "location": "San Francisco"
    }

    # Make the PATCH request
    try:
        response = requests.patch(f"{BASE_URL}{UPDATE_ENDPOINT}", headers=headers, json=data)

        if response.status_code == 200:
            print("User updated successfully!")
            print("Response Data:", response.json())
        else:
            print(f"Failed to update user: {response.status_code}")
            print("Response:", response.json())
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Main Execution
# if __name__ == "__main__":
#     # Step 1: Sign in the user and get the JWT token
#     jwt_token = sign_in_user()

#     if jwt_token:
#         # Step 2: Use the token to update the user's profile
#         update_user_profile()

login = sign_in_user()
update = update_user_profile()