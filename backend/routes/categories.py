from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid
from datetime import datetime

from models import Category, CategoryCreate, CategoryRead
from db import get_session

router = APIRouter()

@router.get("/categories", response_model=dict)
def get_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    categories_read = [CategoryRead.from_orm(category) for category in categories]
    
    return {
        "success": True,
        "data": {
            "categories": categories_read
        }
    }

@router.post("/categories", response_model=dict)
def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    # In a real app, we would get the authenticated user's ID
    # For now, we'll use a placeholder
    db_category = Category.model_validate(category)
    db_category.owner_id = uuid.uuid4()  # Placeholder - should be from auth
    db_category.count = 0
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    
    return {
        "success": True,
        "data": {
            "category": CategoryRead.from_orm(db_category)
        }
    }