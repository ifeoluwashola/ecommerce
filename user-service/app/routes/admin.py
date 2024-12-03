from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import AdminCreate, UserRead, UserUpdate
from app.utils.hashing import get_password_hash, verify_password
from app.utils.auth import create_access_token, require_admin
from app.utils.logging import logger
from app.utils.exceptions import UserNotFoundException, InvalidCredentialsException
from datetime import timedelta
import uuid
from app.db.session import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint: Create Admin User
@router.post("/create", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_admin(
    admin_data: AdminCreate, 
    current_admin: User = Depends(require_admin), 
    db: Session = Depends(get_db)
):
    """
    Create a new admin user. 
    - If no admin exists, the first admin can be created without authentication.
    - For subsequent admins, only authenticated admins can create new admins.
    """
    existing_admin = db.query(User).filter(User.is_admin == True).first()
    if existing_admin and not current_admin or not current_admin.is_admin:
            logger.warning(f"Access denied: {User.role} is not authorized to create an admin")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to create an admin."
            )

    existing_user = db.query(User).filter(User.email == admin_data.email).first()
    if existing_user:
        logger.warning(f"Email {User.email} already exist")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )

    hashed_password = get_password_hash(admin_data.password)
    new_admin = User(
        id=uuid.uuid4(),
        email=admin_data.email,
        hashed_password=hashed_password,
        first_name=admin_data.first_name,
        last_name=admin_data.last_name,
        phone_number=admin_data.phone_number,
        role = "admin",
        is_admin=True
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    logger.info(f"New admin registered: {new_admin.email} by {current_admin.email}.")
    return UserRead.model_validate(new_admin)

# Endpoint: Admin Login
@router.post("/login")
async def admin_login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Admin-specific login endpoint.
    """
    admin = db.query(User).filter(User.email == email, User.is_admin == True).first()
    if not admin or not verify_password(password, admin.hashed_password):
        logger.warning(f"Failed admin login attempt for email: {email}.")
        raise InvalidCredentialsException()

    access_token = create_access_token(
        data={"sub": str(admin.id), "role": "admin"},
        expires_delta=timedelta(minutes=30)
    )
    logger.info(f"Admin {email} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer", "user": UserRead.model_validate(admin)}

# Endpoint: Manage Normal Users
@router.get("/users", dependencies=[Depends(require_admin)])
async def list_users(current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """
    List all normal users (buyers and sellers).
    """
    users = db.query(User).filter(User.is_admin == False).all()
    logger.info(f"Admin {current_admin.email} listed all users.")
    return {"users": [UserRead.model_validate(user) for user in users]}

@router.patch("/users/{user_id}")
async def update_user(
    user_id: str,
    update_data: UserUpdate,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Update user details. Admins can update buyer/seller details.
    """
    user = db.query(User).filter(User.id == user_id, User.is_admin == False).first()
    if not user:
        logger.warning(f"Admin {current_admin.email} attempted to update non-existent user: {user_id}.")
        raise UserNotFoundException()

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    logger.info(f"Admin {current_admin.email} updated user {user_id}.")
    return {"message": "User updated successfully.", "user": UserRead.model_validate(user)}

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Delete a user account. Admins can delete buyer/seller accounts.
    """
    user = db.query(User).filter(User.id == user_id, User.is_admin == False).first()
    if not user:
        logger.warning(f"Admin {current_admin.email} attempted to delete non-existent user: {user_id}.")
        raise UserNotFoundException()

    db.delete(user)
    db.commit()
    logger.info(f"Admin {current_admin.email} deleted user {user_id}.")
    return {"message": "User deleted successfully."}

# Endpoint: View Logs
@router.get("/logs")
async def view_logs(current_admin: User = Depends(require_admin)):
    """
    Fetch application logs.
    """
    try:
        with open("logs/audit.log", "r") as log_file:
            logs = log_file.readlines()
        logger.info(f"Admin {current_admin.email} viewed logs.")
        return {"logs": logs}
    except FileNotFoundError:
        logger.error("Logs file not found.")
        raise HTTPException(status_code=404, detail="Logs not found.")
