from sqlmodel import SQLModel, Session
from contextlib import contextmanager
from typing import Generator
from database import engine

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(bind=engine)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session