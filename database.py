from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator 


DATABASE_URL = "mysql+pymysql://root:admin%40123@127.0.0.1:3306/music_db"


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
