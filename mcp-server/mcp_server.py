from mcp import Server
from mcp.types import Notification, Result, Tool
from mcp.shared_params import Prompt
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import uuid
from datetime import datetime
from contextlib import contextmanager

# Import our models and database functions
from models import Todo, TodoCreate, TodoUpdate, TodoRead, User, UserRead
from db import get_session, create_db_and_tables

# Initialize MCP server
server = Server("todo-chatbot")

# Request/Response models for our tools
class CreateTodoRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[str] = None
    category: Optional[str] = None

class CreateTodoResult(BaseModel):
    success: bool
    todo: Optional[TodoRead] = None
    error: Optional[str] = None

class GetTodosRequest(BaseModel):
    status_filter: Optional[str] = None  # "all", "active", "completed"
    priority_filter: Optional[str] = None
    category_filter: Optional[str] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0

class GetTodosResult(BaseModel):
    success: bool
    todos: List[TodoRead] = []
    error: Optional[str] = None

class UpdateTodoRequest(BaseModel):
    todo_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    category: Optional[str] = None

class UpdateTodoResult(BaseModel):
    success: bool
    todo: Optional[TodoRead] = None
    error: Optional[str] = None

class DeleteTodoRequest(BaseModel):
    todo_id: str

class DeleteTodoResult(BaseModel):
    success: bool
    error: Optional[str] = None

class ToggleTodoCompletionRequest(BaseModel):
    todo_id: str

class ToggleTodoCompletionResult(BaseModel):
    success: bool
    todo: Optional[TodoRead] = None
    error: Optional[str] = None

class GetTodoStatsResult(BaseModel):
    success: bool
    total: int = 0
    completed: int = 0
    pending: int = 0
    overdue: int = 0
    error: Optional[str] = None

class GetUserProfileResult(BaseModel):
    success: bool
    user: Optional[UserRead] = None
    error: Optional[str] = None

# Tool implementations
@server.register_tool
def create_todo(request: CreateTodoRequest) -> Result[CreateTodoResult]:
    """
    Creates a new todo item.
    
    Args:
        title: The title of the todo
        description: Optional description
        priority: Priority level (low, medium, high, urgent)
        due_date: Optional due date in ISO format
        category: Optional category
    """
    try:
        # For demo purposes, we'll use a placeholder user ID
        # In a real implementation, this would come from authentication context
        owner_id = uuid.uuid4()
        
        # Convert due_date string to datetime if provided
        due_date_obj = None
        if request.due_date:
            due_date_obj = datetime.fromisoformat(request.due_date.replace('Z', '+00:00'))
        
        # Create todo data
        todo_data = Todo(
            title=request.title,
            description=request.description,
            priority=request.priority,
            due_date=due_date_obj,
            category=request.category,
            owner_id=owner_id  # In real implementation, this would be from authenticated user
        )
        
        # Create todo in database
        with get_session() as session:
            session.add(todo_data)
            session.commit()
            session.refresh(todo_data)
            
            # Convert to TodoRead format
            todo_read = TodoRead(
                id=todo_data.id,
                title=todo_data.title,
                description=todo_data.description,
                completed=todo_data.completed,
                priority=todo_data.priority,
                due_date=todo_data.due_date,
                category=todo_data.category,
                owner_id=todo_data.owner_id,
                created_at=todo_data.created_at,
                updated_at=todo_data.updated_at
            )
        
        return Result(
            result=CreateTodoResult(success=True, todo=todo_read)
        )
    except Exception as e:
        return Result(
            result=CreateTodoResult(success=False, error=str(e))
        )

@server.register_tool
def get_todos(request: GetTodosRequest) -> Result[GetTodosResult]:
    """
    Retrieves user's todo items with optional filters.
    
    Args:
        status_filter: Filter by status (all, active, completed)
        priority_filter: Filter by priority level
        category_filter: Filter by category
        limit: Maximum number of results
        offset: Offset for pagination
    """
    try:
        # For demo purposes, we'll use a placeholder user ID
        # In a real implementation, this would come from authentication context
        owner_id = uuid.uuid4()
        
        # Query the database with filters
        from sqlmodel import select
        
        with get_session() as session:
            # Build query with filters
            query = select(Todo).where(Todo.owner_id == owner_id)
            
            if request.status_filter:
                if request.status_filter == "active":
                    query = query.where(Todo.completed == False)
                elif request.status_filter == "completed":
                    query = query.where(Todo.completed == True)
            
            if request.priority_filter:
                query = query.where(Todo.priority == request.priority_filter)
                
            if request.category_filter:
                query = query.where(Todo.category == request.category_filter)
            
            # Apply pagination
            query = query.limit(request.limit).offset(request.offset)
            
            # Execute query
            todos = session.exec(query).all()
            
            # Convert to TodoRead format
            todos_read = [
                TodoRead(
                    id=todo.id,
                    title=todo.title,
                    description=todo.description,
                    completed=todo.completed,
                    priority=todo.priority,
                    due_date=todo.due_date,
                    category=todo.category,
                    owner_id=todo.owner_id,
                    created_at=todo.created_at,
                    updated_at=todo.updated_at
                )
                for todo in todos
            ]
        
        return Result(
            result=GetTodosResult(success=True, todos=todos_read)
        )
    except Exception as e:
        return Result(
            result=GetTodosResult(success=False, error=str(e))
        )

@server.register_tool
def update_todo(request: UpdateTodoRequest) -> Result[UpdateTodoResult]:
    """
    Updates an existing todo item.
    
    Args:
        todo_id: ID of the todo to update
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)
        priority: New priority (optional)
        due_date: New due date (optional)
        category: New category (optional)
    """
    try:
        # For demo purposes, we'll use a placeholder user ID
        # In a real implementation, this would come from authentication context
        owner_id = uuid.uuid4()
        
        # Validate the todo_id
        try:
            todo_uuid = uuid.UUID(request.todo_id)
        except ValueError:
            return Result(
                result=UpdateTodoResult(success=False, error="Invalid todo ID format")
            )
        
        # Update the database record
        with get_session() as session:
            # Get the existing todo
            todo = session.get(Todo, todo_uuid)
            if not todo:
                return Result(
                    result=UpdateTodoResult(success=False, error="Todo not found")
                )
            
            # Check if the user owns this todo (in a real implementation)
            if todo.owner_id != owner_id:
                return Result(
                    result=UpdateTodoResult(success=False, error="Not authorized to update this todo")
                )
            
            # Update fields that were provided
            if request.title is not None:
                todo.title = request.title
            if request.description is not None:
                todo.description = request.description
            if request.completed is not None:
                todo.completed = request.completed
            if request.priority is not None:
                todo.priority = request.priority
            if request.due_date is not None:
                todo.due_date = datetime.fromisoformat(request.due_date.replace('Z', '+00:00'))
            if request.category is not None:
                todo.category = request.category
            
            # Update the timestamp
            todo.updated_at = datetime.utcnow()
            
            # Commit changes
            session.add(todo)
            session.commit()
            session.refresh(todo)
            
            # Convert to TodoRead format
            todo_read = TodoRead(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
                priority=todo.priority,
                due_date=todo.due_date,
                category=todo.category,
                owner_id=todo.owner_id,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
        
        return Result(
            result=UpdateTodoResult(success=True, todo=todo_read)
        )
    except Exception as e:
        return Result(
            result=UpdateTodoResult(success=False, error=str(e))
        )

@server.register_tool
def delete_todo(request: DeleteTodoRequest) -> Result[DeleteTodoResult]:
    """
    Deletes a todo item.
    
    Args:
        todo_id: ID of the todo to delete
    """
    try:
        # For demo purposes, we'll use a placeholder user ID
        # In a real implementation, this would come from authentication context
        owner_id = uuid.uuid4()
        
        # Validate the todo_id
        try:
            todo_uuid = uuid.UUID(request.todo_id)
        except ValueError:
            return Result(
                result=DeleteTodoResult(success=False, error="Invalid todo ID format")
            )
        
        # Delete from the database
        with get_session() as session:
            # Get the existing todo
            todo = session.get(Todo, todo_uuid)
            if not todo:
                return Result(
                    result=DeleteTodoResult(success=False, error="Todo not found")
                )
            
            # Check if the user owns this todo (in a real implementation)
            if todo.owner_id != owner_id:
                return Result(
                    result=DeleteTodoResult(success=False, error="Not authorized to delete this todo")
                )
            
            # Delete the todo
            session.delete(todo)
            session.commit()
        
        return Result(
            result=DeleteTodoResult(success=True)
        )
    except Exception as e:
        return Result(
            result=DeleteTodoResult(success=False, error=str(e))
        )

@server.register_tool
def toggle_todo_completion(request: ToggleTodoCompletionRequest) -> Result[ToggleTodoCompletionResult]:
    """
    Toggles the completion status of a todo item.
    
    Args:
        todo_id: ID of the todo to toggle
    """
    try:
        # For demo purposes, we'll use a placeholder user ID
        # In a real implementation, this would come from authentication context
        owner_id = uuid.uuid4()
        
        # Validate the todo_id
        try:
            todo_uuid = uuid.UUID(request.todo_id)
        except ValueError:
            return Result(
                result=ToggleTodoCompletionResult(success=False, error="Invalid todo ID format")
            )
        
        # Toggle completion status in the database
        with get_session() as session:
            # Get the existing todo
            todo = session.get(Todo, todo_uuid)
            if not todo:
                return Result(
                    result=ToggleTodoCompletionResult(success=False, error="Todo not found")
                )
            
            # Check if the user owns this todo (in a real implementation)
            if todo.owner_id != owner_id:
                return Result(
                    result=ToggleTodoCompletionResult(success=False, error="Not authorized to update this todo")
                )
            
            # Toggle the completion status
            todo.completed = not todo.completed
            todo.updated_at = datetime.utcnow()
            
            # Commit changes
            session.add(todo)
            session.commit()
            session.refresh(todo)
            
            # Convert to TodoRead format
            todo_read = TodoRead(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
                priority=todo.priority,
                due_date=todo.due_date,
                category=todo.category,
                owner_id=todo.owner_id,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
        
        return Result(
            result=ToggleTodoCompletionResult(success=True, todo=todo_read)
        )
    except Exception as e:
        return Result(
            result=ToggleTodoCompletionResult(success=False, error=str(e))
        )

@server.register_tool
def get_todo_stats() -> Result[GetTodoStatsResult]:
    """
    Gets user's todo statistics.
    """
    try:
        # For demo purposes, we'll use a placeholder user ID
        # In a real implementation, this would come from authentication context
        owner_id = uuid.uuid4()
        
        # Query the database for stats
        from sqlmodel import select
        from datetime import datetime
        
        with get_session() as session:
            # Get total count
            total_query = select(Todo).where(Todo.owner_id == owner_id)
            total = len(session.exec(total_query).all())
            
            # Get completed count
            completed_query = select(Todo).where(Todo.owner_id == owner_id, Todo.completed == True)
            completed = len(session.exec(completed_query).all())
            
            # Calculate pending
            pending = total - completed
            
            # Get overdue count (todos that are not completed and past due date)
            overdue_query = select(Todo).where(
                Todo.owner_id == owner_id,
                Todo.completed == False,
                Todo.due_date < datetime.utcnow()
            )
            overdue = len(session.exec(overdue_query).all())
        
        return Result(
            result=GetTodoStatsResult(
                success=True,
                total=total,
                completed=completed,
                pending=pending,
                overdue=overdue
            )
        )
    except Exception as e:
        return Result(
            result=GetTodoStatsResult(success=False, error=str(e))
        )

@server.register_tool
def get_user_profile() -> Result[GetUserProfileResult]:
    """
    Retrieves user information.
    """
    try:
        # For demo purposes, we'll use a placeholder user ID
        # In a real implementation, this would come from authentication context
        user_id = uuid.uuid4()
        
        # Get user data from the database
        with get_session() as session:
            user = session.get(User, user_id)
            if not user:
                return Result(
                    result=GetUserProfileResult(success=False, error="User not found")
                )
            
            # Convert to UserRead format
            user_read = UserRead(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        
        return Result(
            result=GetUserProfileResult(success=True, user=user_read)
        )
    except Exception as e:
        return Result(
            result=GetUserProfileResult(success=False, error=str(e))
        )

# Health check notification
@server.set_initialization_options
def initialization_options():
    # Initialize database tables
    create_db_and_tables()
    return {
        "capabilities": {
            "tools": {
                "execute": {},
                "list": {}
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server.app, host="0.0.0.0", port=8001)