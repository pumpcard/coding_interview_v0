import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = os.environ.get("PUMP_DATABASE_URL", default="postgresql://pump:pump@localhost:5432/pump")
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_database() -> SessionLocal:
    """
    Get the database session and ensure closing it afterward
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
