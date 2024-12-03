from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.hashing import get_password_hash
from app.db.session import SessionLocal
import uuid

def create_first_admin():
    db: Session = SessionLocal()
    try:
        # Check if an admin already exists
        existing_admin = db.query(User).filter(User.is_admin == True).first()
        if existing_admin:
            print("An admin already exists. No action taken.")
            return

        # Define admin details
        admin_data = {
            "id": uuid.uuid4(),
            "email": "ifeoluwashola06@gmail.com",  # Replace with your desired email
            "hashed_password": get_password_hash("Ifebabis.1"),  # Replace with your desired password
            "first_name": "Ifeoluwa",
            "last_name": "Adaralegbe",
            "phone_number": "+2348130710195",  # Replace with your desired phone number
            "is_admin": True,
        }

        # Create admin
        admin = User(**admin_data)
        db.add(admin)
        db.commit()
        print(f"Admin {admin.email} created successfully.")
    except Exception as e:
        print(f"Error creating admin: {e}")
    finally:
        db.close()

# Run the script
if __name__ == "__main__":
    create_first_admin()
