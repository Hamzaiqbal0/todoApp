from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import SQLModel, Field, create_engine, Session, select
from contextlib import contextmanager
from typing import Optional, Generator
import os
from datetime import datetime
import uuid
from pydantic import BaseModel

# Simple model without complex relationships
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: int = Field(default=None, primary_key=True)  # Changed to int for simplicity
    password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

# Database setup
DATABASE_URL = "sqlite:///./todoapp_simple.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/api/auth/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create new user (without password hashing for simplicity)
    db_user = User(
        email=user.email,
        name=user.name,
        password=user.password  # In real app, hash this
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return {
        "success": True,
        "data": {
            "user": UserRead.model_validate(db_user),
            "token": "fake-token-for-testing"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)