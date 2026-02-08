import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
from models import User

load_dotenv()

SECRET_KEY = os.getenv("AUTH_JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
ALGORITHM = os.getenv("AUTH_JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return the payload if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

def get_current_user(token: str) -> Optional[User]:
    """Get the current user from the token"""
    payload = verify_token(token)
    if payload:
        # In a real implementation, we'd query the database for the user
        # For now, we'll return a mock user
        user_id = payload.get("sub")
        if user_id:
            # This would be replaced with a database query:
            # user = session.get(User, user_id)
            # return user
            return User(
                id=user_id,
                email=payload.get("email", "user@example.com"),
                name=payload.get("name", "Demo User"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
    return None