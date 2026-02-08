from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List
import uuid

# User Models
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

# Todo Models
class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # low, medium, high, urgent
    due_date: Optional[datetime] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []

class Todo(TodoBase, table=True):
    __tablename__ = "todos"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

# Category Models
class CategoryBase(SQLModel):
    name: str = Field(unique=True, index=True)
    color: str

class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    count: int = 0  # Number of todos in this category
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    count: int
    created_at: datetime