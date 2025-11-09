from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

def get_engine(database_url: str = settings.DATABASE_URL):
    return create_engine(database_url)

def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = get_engine()
SessionLocal = get_session_local(engine)
Base = declarative_base()