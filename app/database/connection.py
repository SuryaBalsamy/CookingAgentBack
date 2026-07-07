import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and "?ssl-mode=REQUIRED" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("?ssl-mode=REQUIRED", "")

engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {}}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
