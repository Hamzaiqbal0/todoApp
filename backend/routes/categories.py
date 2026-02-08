from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List
import uuid
from datetime import datetime

from models import Category, CategoryCreate, CategoryRead, User
from db import get_session
from routes.auth import get_current_user

router = APIRouter()

@router.get("/categories", response_model=dict)
def get_categories(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    categories = session.exec(select(Category).where(Category.owner_id == current_user.id)).all()
    categories_read = [CategoryRead.model_validate(category) for category in categories]
    
    return {
        "success": True,
        "data": {
            "categories": categories_read
        }
    }

@router.post("/categories", response_model=dict)
def create_category(category: CategoryCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    db_category = Category.model_validate(category)
    db_category.owner_id = current_user.id  # Associate with authenticated user
    db_category.count = 0
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    
    return {
        "success": True,
        "data": {
            "category": CategoryRead.model_validate(db_category)
        }
    }