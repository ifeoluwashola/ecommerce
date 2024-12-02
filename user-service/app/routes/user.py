from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserRead, UserUpdate
from app.models import User
from app.db.session import SessionLocal
from app.utils.hashing import get_password_hash, verify_password
import uuid
from app.utils.auth import create_access_token, get_current_user, require_role, decode_access_token
from datetime import timedelta
from app.utils.hashing import get_password_hash
from app.utils.email import send_email
from pathlib import Path
import shutil
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create user object
    new_user = User(
        id=uuid.uuid4(),
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        role=user.role,
    )
    
    # Add to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(request: Request, email: str, password: str, db: Session = Depends(get_db)):
    # Check if the user exists
    """ Login endpoint with rate limiting applied."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    
    # Verify the password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role},
        expires_delta=timedelta(minutes=30),
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserRead.model_validate(user),  # Return user details (excluding sensitive data)
    }

@router.get("/profile", tags=["Private"])
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Retrieve the authenticated user's profile.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
    }

@router.put("/profile", response_model=UserRead)
async def edit_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Edit user profile fields like email, phone number, or name.
    """
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already in use.")
        current_user.email = user_update.email

    if user_update.phone_number and user_update.phone_number != current_user.phone_number:
        existing_user = db.query(User).filter(User.phone_number == user_update.phone_number).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number is already in use.")
        current_user.phone_number = user_update.phone_number

    # Update other fields
    current_user.first_name = user_update.first_name or current_user.first_name
    current_user.last_name = user_update.last_name or current_user.last_name

    db.commit()
    db.refresh(current_user)

    return UserRead.model_validate(current_user)

@router.get("/seller-dashboard", tags=["Private"])
def seller_dashboard(current_user: User = Depends(require_role("seller"))):
    """
    Access restricted to sellers only.
    """
    return {"message": f"Welcome to the seller dashboard, {current_user.first_name}!"}

@router.post("/password-reset/request")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=15))
    await send_email(to=user.email, subject="Password Reset", body=f"Reset token: {token}")
    return {"message": "Password reset email sent."}

@router.post("/password-reset/confirm")
async def confirm_password_reset(token: str, new_password: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return {"message": "Password updated successfully."}

UPLOAD_FOLDER = Path("static/avatars")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists

@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upload or update the user's avatar.
    Args:
        file (UploadFile): The image file uploaded by the user.
        current_user (User): The authenticated user making the request.
    Returns:
        dict: A message indicating success or failure.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    # Define the file path
    avatar_path = UPLOAD_FOLDER / f"{current_user.id}.jpg"
    
    # Save the file
    with open(avatar_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Update user's avatar_url in the database
    current_user.avatar_url = str(avatar_path)
    db.commit()

    return {"message": "Avatar uploaded successfully.", "avatar_url": current_user.avatar_url}
