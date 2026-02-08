from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import BaseModel

from models import User, UserCreate, UserRead
from db import get_session

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = session.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(session: Session = Depends(get_session)):
    # This is a simplified version - in a real app, you'd decode the JWT from headers
    # and return the corresponding user
    pass

@router.post("/auth/register", response_model=dict)
def register(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create new user
    db_user = User(
        email=user.email,
        name=user.name,
        password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    
    return {
        "success": True,
        "data": {
            "user": UserRead.from_orm(db_user),
            "token": access_token
        }
    }

@router.post("/auth/login", response_model=dict)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    user = authenticate_user(session, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "success": True,
        "data": {
            "user": UserRead.from_orm(user),
            "token": access_token
        }
    }

@router.post("/auth/logout")
def logout():
    # In a real implementation, you might invalidate tokens here
    return {"success": True, "message": "Logged out successfully"}