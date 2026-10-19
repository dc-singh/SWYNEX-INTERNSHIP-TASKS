from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL is missing from the .env file")


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()