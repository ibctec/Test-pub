"""
Database engine - SQlite4
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from emp.schemas import Base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    """Ensure database tables are created"""
    Base.metadata.create_all(bind=engine)


def clear_db():
    """Clear DB"""
    Base.metadata.drop_all(engine)
