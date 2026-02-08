from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime

from models import Todo, TodoCreate, TodoRead, TodoUpdate
from db import get_session

router = APIRouter()

@router.get("/todos", response_model=dict)
def get_todos(
    session: Session = Depends(get_session),
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("created_at"),
    order: Optional[str] = Query("desc"),
    page: Optional[int] = Query(1),
    limit: Optional[int] = Query(10)
):
    query = select(Todo)
    
    # Apply filters
    if status_filter and status_filter != "all":
        if status_filter == "active":
            query = query.where(Todo.completed == False)
        elif status_filter == "completed":
            query = query.where(Todo.completed == True)
    
    if priority:
        query = query.where(Todo.priority == priority)
    
    if category:
        query = query.where(Todo.category == category)
    
    if search:
        query = query.where(Todo.title.contains(search) | Todo.description.contains(search))
    
    # Apply sorting
    if sort == "due_date":
        query = query.order_by(Todo.due_date.desc() if order == "desc" else Todo.due_date.asc())
    elif sort == "priority":
        query = query.order_by(Todo.priority.desc() if order == "desc" else Todo.priority.asc())
    elif sort == "title":
        query = query.order_by(Todo.title.desc() if order == "desc" else Todo.title.asc())
    else:  # default to created_at
        query = query.order_by(Todo.created_at.desc() if order == "desc" else Todo.created_at.asc())
    
    # Pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    
    todos = session.exec(query).all()
    todos_read = [TodoRead.from_orm(todo) for todo in todos]
    
    # Calculate total for pagination info
    count_query = select(Todo)
    if status_filter and status_filter != "all":
        if status_filter == "active":
            count_query = count_query.where(Todo.completed == False)
        elif status_filter == "completed":
            count_query = count_query.where(Todo.completed == True)
    
    if priority:
        count_query = count_query.where(Todo.priority == priority)
    
    if category:
        count_query = count_query.where(Todo.category == category)
    
    if search:
        count_query = count_query.where(Todo.title.contains(search) | Todo.description.contains(search))
    
    total = session.exec(count_query).count()
    
    return {
        "success": True,
        "data": {
            "todos": todos_read,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        }
    }

@router.get("/todos/{id}", response_model=dict)
def get_todo(id: str, session: Session = Depends(get_session)):
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
        
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {
        "success": True,
        "data": {
            "todo": TodoRead.from_orm(todo)
        }
    }

@router.post("/todos", response_model=dict)
def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    # In a real app, we would get the authenticated user's ID
    # For now, we'll use a placeholder
    db_todo = Todo.model_validate(todo)
    db_todo.owner_id = uuid.uuid4()  # Placeholder - should be from auth
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    
    return {
        "success": True,
        "data": {
            "todo": TodoRead.from_orm(db_todo)
        }
    }

@router.put("/todos/{id}", response_model=dict)
def update_todo(id: str, todo_update: TodoUpdate, session: Session = Depends(get_session)):
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update fields
    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    
    return {
        "success": True,
        "data": {
            "todo": TodoRead.from_orm(db_todo)
        }
    }

@router.patch("/todos/{id}/toggle", response_model=dict)
def toggle_todo(id: str, session: Session = Depends(get_session)):
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Toggle completion status
    db_todo.completed = not db_todo.completed
    db_todo.updated_at = datetime.utcnow()
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    
    return {
        "success": True,
        "data": {
            "todo": TodoRead.from_orm(db_todo)
        }
    }

@router.delete("/todos/{id}")
def delete_todo(id: str, session: Session = Depends(get_session)):
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    session.delete(db_todo)
    session.commit()
    
    return {
        "success": True,
        "message": "Todo deleted successfully"
    }