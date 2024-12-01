from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserRead
from app.models import User
from app.db.session import SessionLocal
from app.utils.hashing import get_password_hash, verify_password
import uuid
from app.utils.auth import create_access_token, get_current_user, require_role
from datetime import timedelta

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
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
def login(email: str, password: str, db: Session = Depends(get_db)):
    # Check if the user exists
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
        "user": UserRead.from_orm(user),  # Return user details (excluding sensitive data)
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

@router.get("/seller-dashboard", tags=["Private"])
def seller_dashboard(current_user: User = Depends(require_role("seller"))):
    """
    Access restricted to sellers only.
    """
    return {"message": f"Welcome to the seller dashboard, {current_user.first_name}!"}