from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User, UserTranspose, PasswordResetToken # Import PasswordResetToken
from schemas import users
from fastapi import HTTPException, status
from passlib.context import CryptContext
import models
from JWTtoken import create_access_token
from datetime import datetime, timedelta # Added datetime and timedelta
import uuid # Added uuid
from typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def user_signup(data: users.UserSignup, db: Session):
    user_exists = db.query(User).filter(User.email == data.email).first()

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    hashed_password = hash_password(data.password)

    db_user = User(name=data.name, email=data.email, password=hashed_password)
    db.add(db_user)

    db.commit()
    db.refresh(db_user)

    return db_user


def user_sign(data: users.UserSignin, db: Session):
    user_in_db = db.query(User).filter(User.email == data.email).first()

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

    if verify_password(data.password, user_in_db.password):  # type: ignore
        access_token = create_access_token(data={"user_id": str(user_in_db.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "name":user_in_db.name,
            "message": "You are logged in successfully!"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

# New function to create a password reset token
def create_password_reset_token(email: str, db: Session) -> Optional[str]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None # Return None if user not found, to avoid disclosing email existence

    # Invalidate any existing tokens for this user for security
    db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user.id).delete()

    token = str(uuid.uuid4()) # Generate a unique token
    expires_at = datetime.utcnow() + timedelta(hours=1) # Token valid for 1 hour

    new_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return token

# New function to reset user password
def reset_user_password(token: str, new_password: str, db: Session) -> bool:
    reset_token_entry = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token,
        PasswordResetToken.expires_at > datetime.utcnow() # Check if token is not expired
    ).first()

    if not reset_token_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token."
        )

    user = db.query(User).filter(User.id == reset_token_entry.user_id).first()
    if not user:
        # This should theoretically not happen if foreign key constraints are correct
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User not found for the given token."
        )

    user.password = hash_password(new_password) # type: ignore
    db.delete(reset_token_entry) # Invalidate and delete the token after use
    db.commit()
    return True

def add_user_transpose(user_id: str, transpose_str: str,note_str: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    new_transpose = UserTranspose(
        user_id=user_id,
        transpose=transpose_str,
        notes=note_str
    )
    db.add(new_transpose)
    db.commit()
    db.refresh(new_transpose)
    return new_transpose

def get_transpose(user_id:str ,db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transposes = db.query(models.UserTranspose).filter(models.UserTranspose.user_id == user_id).all()

    return {
        "user_id": user_id,
        "transpositions": [
            {
                "notes": transpose.notes,
                "transpose": transpose.transpose
            } for transpose in transposes
        ]
    }