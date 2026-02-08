from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from models import User, UserCreate, UserRead
from db import get_session

load_dotenv()

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings - using environment variable or default
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(request: Request, session: Session = Depends(get_session)):
    token_str = request.headers.get("Authorization")
    if not token_str or not token_str.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = token_str.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = session.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.post("/auth/register", response_model=dict)
def register(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
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
    
    user_data = {
        "id": str(db_user.id),
        "email": db_user.email,
        "name": db_user.name,
        "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
        "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None
    }
    
    return {
        "success": True,
        "data": {
            "user": user_data,
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
    
    user_data = {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }
    
    return {
        "success": True,
        "data": {
            "user": user_data,
            "token": access_token
        }
    }

@router.post("/auth/logout")
def logout():
    # In a real implementation, you might invalidate tokens here
    # For now, we just return a success message
    return {"success": True, "message": "Logged out successfully"}