import uuid
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUIDs are 36 chars
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)

    transposes = relationship("UserTranspose", back_populates="user", cascade="all, delete")


class UserTranspose(Base):
    __tablename__ = "transposes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    notes=Column(Text)
    transpose = Column(Text)

    user = relationship("User", back_populates="transposes")
