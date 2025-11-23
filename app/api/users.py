# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from pydantic import BaseModel, EmailStr
from typing import List

router = APIRouter()


# Pydantic schemas for request/response
class UserCreate(BaseModel):
    """Schema for creating a user"""

    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response (no password!)"""

    id: int
    email: str
    username: str
    is_active: bool

    class Config:
        from_attributes = True  # Allow ORM models


# Endpoints
@router.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    """

    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create new user (TODO: hash password properly later)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=user.password,  # WARNING: Not hashed yet! We'll fix this tomorrow
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/users/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get list of users
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get specific user by ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
