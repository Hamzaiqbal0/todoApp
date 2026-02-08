from sqlmodel import SQLModel, Field, create_engine, Session, select
from contextlib import contextmanager
from typing import Optional, Generator
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todoapp.db")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session