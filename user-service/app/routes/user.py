from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserRead, UserUpdate
from app.models import User
from app.db.session import SessionLocal
from app.utils.hashing import get_password_hash, verify_password
import uuid
from app.utils.auth import create_access_token, get_current_user, require_role, decode_access_token
from datetime import timedelta
from app.utils.email import send_email
from pathlib import Path
import shutil
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.utils.logging import logger
from app.utils.exceptions import UserNotFoundException, InvalidCredentialsException

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint: Register User
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logger.warning(f"Registration failed: Email {user.email} already registered.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        id=uuid.uuid4(),
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"New user registered with email {user.email}.")
    return new_user

# Endpoint: User Login
@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(request: Request, email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        logger.warning(f"Failed login attempt for email {email}.")
        raise InvalidCredentialsException()
    
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Failed login attempt for email {email}. Incorrect password.")
        raise InvalidCredentialsException()

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role},
        expires_delta=timedelta(minutes=30),
    )
    logger.info(f"User {email} logged in successfully.")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserRead.model_validate(user),
    }

# Endpoint: Get User Profile
@router.get("/profile", tags=["Private"])
def get_user_profile(current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.email} accessed profile.")
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
    }

# Endpoint: Edit User Profile
@router.put("/profile", response_model=UserRead)
async def edit_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            logger.warning(f"Email update failed for user {current_user.email}: Email {user_update.email} is already in use.")
            raise HTTPException(status_code=400, detail="Email is already in use.")
        current_user.email = user_update.email

    if user_update.phone_number and user_update.phone_number != current_user.phone_number:
        existing_user = db.query(User).filter(User.phone_number == user_update.phone_number).first()
        if existing_user:
            logger.warning(f"Phone number update failed for user {current_user.email}: Phone number {user_update.phone_number} is already in use.")
            raise HTTPException(status_code=400, detail="Phone number is already in use.")
        current_user.phone_number = user_update.phone_number

    current_user.first_name = user_update.first_name or current_user.first_name
    current_user.last_name = user_update.last_name or current_user.last_name

    db.commit()
    db.refresh(current_user)
    logger.info(f"User {current_user.email} updated profile.")
    return UserRead.model_validate(current_user)

# Endpoint: Seller Dashboard
@router.get("/seller-dashboard", tags=["Private"])
def seller_dashboard(current_user: User = Depends(require_role("seller"))):
    logger.info(f"Seller {current_user.email} accessed the seller dashboard.")
    return {"message": f"Welcome to the seller dashboard, {current_user.first_name}!"}

# Endpoint: Password Reset Request
@router.post("/password-reset/request")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Password reset requested for non-existent email {email}.")
        raise UserNotFoundException()

    token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=15))
    await send_email(to=user.email, subject="Password Reset", body=f"Reset token: {token}")
    logger.info(f"Password reset email sent to {email}.")
    return {"message": "Password reset email sent."}

# Endpoint: Confirm Password Reset
@router.post("/password-reset/confirm")
async def confirm_password_reset(token: str, new_password: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Password reset failed: Email {email} not found.")
        raise UserNotFoundException()

    user.hashed_password = get_password_hash(new_password)
    db.commit()
    logger.info(f"Password reset successful for {email}.")
    return {"message": "Password updated successfully."}

# Endpoint: Upload Avatar
UPLOAD_FOLDER = Path("static/avatars")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.content_type.startswith("image/"):
        logger.warning(f"Avatar upload failed for {current_user.email}: Invalid file type {file.content_type}.")
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    avatar_path = UPLOAD_FOLDER / f"{current_user.id}.jpg"
    with open(avatar_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    current_user.avatar_url = str(avatar_path)
    db.commit()
    logger.info(f"Avatar uploaded for user {current_user.email}.")
    return {"message": "Avatar uploaded successfully.", "avatar_url": current_user.avatar_url}

# Endpoint: Refresh Token
@router.post("/token/refresh")
async def refresh_token(refresh_token: str):
    payload = decode_access_token(refresh_token)
    if not payload:
        logger.warning("Invalid or expired refresh token.")
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token.")

    new_access_token = create_access_token({"sub": payload["sub"], "role": payload["role"]})
    logger.info("Refresh token issued successfully.")
    return {"access_token": new_access_token, "token_type": "bearer"}
