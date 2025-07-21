import uuid
from sqlalchemy import Column, String, ForeignKey, Text, DateTime # Added DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta # Added datetime and timedelta


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUIDs are 36 chars
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)

    transposes = relationship("UserTranspose", back_populates="user", cascade="all, delete")
    # New relationship for password reset tokens
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete")


class UserTranspose(Base):
    __tablename__ = "transposes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    notes=Column(Text)
    transpose = Column(Text)

    user = relationship("User", back_populates="transposes")

# New model for Password Reset Tokens
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="password_reset_tokens")