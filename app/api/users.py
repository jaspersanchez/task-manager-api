# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.security import get_password_hash
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Create new user with HASHED password
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password),  # HASHED
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user

    This endpoint requires authentication!
    """
    return current_user


@router.get("/users/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 10,
    email: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),  # PROTECTED
):
    """
    Get list of users (requires authentication)
    """
    query = db.query(User)

    if email:
        query = query.filter(User.email.contains(email))

    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),  # PROTECTED
):
    """
    Get specific user by ID (requires authentication)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),  # PROTECTED
):
    """
    Delete a user (requires authentication)

    Users can only delete themselves unless they're superuser
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Check permission: can only delete self unless superuser
    if user.id != current_user.id and not current_user.is_superuser:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    db.delete(user)
    db.commit()

    return None
