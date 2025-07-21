from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator
import os


# --- REMOVE THE FALLBACK VALUE HERE ---
DATABASE_URL = os.getenv("DATABASE_URL")

# --- IMPORTANT: Add a check to ensure the URL is loaded ---
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Please configure your .env file.")
# --------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()