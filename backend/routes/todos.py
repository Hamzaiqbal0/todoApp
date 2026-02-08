from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime

from models import Todo, TodoCreate, TodoRead, TodoUpdate, User
from db import get_session
from routes.auth import get_current_user

router = APIRouter()

@router.get("/todos", response_model=dict)
def get_todos(
    current_user: User = Depends(get_current_user),
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
    query = select(Todo).where(Todo.owner_id == current_user.id)
    
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
    todos_read = [TodoRead.model_validate(todo) for todo in todos]
    
    # Calculate total for pagination info
    count_query = select(Todo).where(Todo.owner_id == current_user.id)
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
    
    # Convert todos to dictionaries
    todos_dict = []
    for todo in todos:
        todos_dict.append({
            "id": str(todo.id),
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "priority": todo.priority,
            "due_date": todo.due_date.isoformat() if todo.due_date else None,
            "category": todo.category,
            "tags": todo.tags,
            "owner_id": str(todo.owner_id),
            "created_at": todo.created_at.isoformat() if todo.created_at else None,
            "updated_at": todo.updated_at.isoformat() if todo.updated_at else None
        })
    
    return {
        "success": True,
        "data": {
            "todos": todos_dict,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        }
    }

@router.get("/todos/{id}", response_model=dict)
def get_todo(id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
        
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Check if the todo belongs to the current user
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")
    
    todo_data = {
        "id": str(todo.id),
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "priority": todo.priority,
        "due_date": todo.due_date.isoformat() if todo.due_date else None,
        "category": todo.category,
        "tags": todo.tags,
        "owner_id": str(todo.owner_id),
        "created_at": todo.created_at.isoformat() if todo.created_at else None,
        "updated_at": todo.updated_at.isoformat() if todo.updated_at else None
    }
    
    return {
        "success": True,
        "data": {
            "todo": todo_data
        }
    }

@router.post("/todos", response_model=dict)
def create_todo(todo: TodoCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    db_todo = Todo.model_validate(todo)
    db_todo.owner_id = current_user.id  # Associate with authenticated user
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    
    todo_data = {
        "id": str(db_todo.id),
        "title": db_todo.title,
        "description": db_todo.description,
        "completed": db_todo.completed,
        "priority": db_todo.priority,
        "due_date": db_todo.due_date.isoformat() if db_todo.due_date else None,
        "category": db_todo.category,
        "tags": db_todo.tags,
        "owner_id": str(db_todo.owner_id),
        "created_at": db_todo.created_at.isoformat() if db_todo.created_at else None,
        "updated_at": db_todo.updated_at.isoformat() if db_todo.updated_at else None
    }
    
    return {
        "success": True,
        "data": {
            "todo": todo_data
        }
    }

@router.put("/todos/{id}", response_model=dict)
def update_todo(id: str, todo_update: TodoUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Check if the todo belongs to the current user
    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    
    # Update fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    
    todo_data = {
        "id": str(db_todo.id),
        "title": db_todo.title,
        "description": db_todo.description,
        "completed": db_todo.completed,
        "priority": db_todo.priority,
        "due_date": db_todo.due_date.isoformat() if db_todo.due_date else None,
        "category": db_todo.category,
        "tags": db_todo.tags,
        "owner_id": str(db_todo.owner_id),
        "created_at": db_todo.created_at.isoformat() if db_todo.created_at else None,
        "updated_at": db_todo.updated_at.isoformat() if db_todo.updated_at else None
    }
    
    return {
        "success": True,
        "data": {
            "todo": todo_data
        }
    }

@router.patch("/todos/{id}/toggle", response_model=dict)
def toggle_todo(id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Check if the todo belongs to the current user
    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    
    # Toggle completion status
    db_todo.completed = not db_todo.completed
    db_todo.updated_at = datetime.utcnow()
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    
    todo_data = {
        "id": str(db_todo.id),
        "title": db_todo.title,
        "description": db_todo.description,
        "completed": db_todo.completed,
        "priority": db_todo.priority,
        "due_date": db_todo.due_date.isoformat() if db_todo.due_date else None,
        "category": db_todo.category,
        "tags": db_todo.tags,
        "owner_id": str(db_todo.owner_id),
        "created_at": db_todo.created_at.isoformat() if db_todo.created_at else None,
        "updated_at": db_todo.updated_at.isoformat() if db_todo.updated_at else None
    }
    
    return {
        "success": True,
        "data": {
            "todo": todo_data
        }
    }

@router.delete("/todos/{id}")
def delete_todo(id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Check if the todo belongs to the current user
    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")
    
    session.delete(db_todo)
    session.commit()
    
    return {
        "success": True,
        "message": "Todo deleted successfully"
    }