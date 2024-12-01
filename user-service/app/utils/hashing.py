from passlib.context import CryptContext

# Create a CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hash a password securely using bcrypt.
    Args:
        password (str): Plain-text password.
    Returns:
        str: Hashed password.
    """
    if not password:
        raise ValueError("Password cannot be empty.")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password.
    Args:
        plain_password (str): Plain-text password to verify.
        hashed_password (str): Hashed password to compare against.
    Returns:
        bool: True if the password matches, False otherwise.
    """
    if not plain_password or not hashed_password:
        raise ValueError("Passwords cannot be empty.")
    return pwd_context.verify(plain_password, hashed_password)


def simulate_user_flow():
    """
    Simulate user registration and login flow to demonstrate password hashing and verification.
    """
    try:
        # User registration simulation
        user_password = input("Enter a new password: ").strip()
        hashed = get_password_hash(user_password)
        print(f"Hashed Password: {hashed}")

        # User login simulation
        login_attempt = input("Enter your password to log in: ").strip()
        if verify_password(login_attempt, hashed):
            print("✅ Password is correct!")
        else:
            print("❌ Password is incorrect.")
    except ValueError as e:
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    simulate_user_flow()
