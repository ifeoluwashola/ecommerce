import requests

# Login and obtain the token
response = requests.post('http://localhost:8002/api/users/login', params={
    'email': 'user@example.com',
    'password': 'newpassword'
})

data = response.json()
access_token = data['access_token']

# Function to get user profile
def get_user_profile():
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    profile_response = requests.get('http://localhost:8002/api/users/profile', headers=headers)
    return profile_response.json()

# Function to get Seller's dashboard if the user role is seller
def get_seller_dashboard():
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    profile_response = requests.get('http://localhost:8002/api/users/seller-dashboard', headers=headers)
    return profile_response.json()

profile_data = get_user_profile()
seller_dashboard = get_seller_dashboard()
print(profile_data)
print(seller_dashboard)

# print(data)