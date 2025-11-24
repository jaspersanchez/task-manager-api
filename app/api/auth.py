# app/api/auth.py
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.models.user import User

router = APIRouter()


# Response schemas
class Token(BaseModel):
    """Token response schema"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data stored in token"""

    user_id: Optional[int] = None


# Endpoints
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login


    Username can be either username or email
    """
    # Try to find user by username
    user = db.query(User).filter(User.username == form_data.username).first()

    # If not found, try email
    user = db.query(User).filter(User.email == form_data.username).first()

    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    """
    Logout endpoint (JWT is stateless, so this is just for client side)

    Cliend should delete the token from storage
    """
    return {"message": "Successfully logged out"}
