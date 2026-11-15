from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utility.settings import settings



base = declarative_base()

engine = create_engine(url=settings.db_url)


local_session = sessionmaker(bind=engine)

def get_db():
    session = local_session()

    try:
        yield session

    finally:
        session.close()