# Database Schema Specifications

## Overview
The Todo application uses Neon PostgreSQL as the primary database with SQLModel as the ORM. The schema is designed to support user authentication, todo management, and categorization features.

## Database Configuration
- **Database**: Neon PostgreSQL
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Connection String**: Retrieved from environment variable `DATABASE_URL`
- **Migration Tool**: Alembic (managed through SQLModel)

## Tables

### 1. Users Table
Stores user account information.

**Table Name**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the user |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| name | VARCHAR(255) | NOT NULL | User's full name |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password using bcrypt |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() ON UPDATE | Last update timestamp |
| is_active | BOOLEAN | DEFAULT TRUE | Account active status |
| email_verified | BOOLEAN | DEFAULT FALSE | Email verification status |

**Indexes**:
- `idx_users_email`: Index on email column for faster lookups
- `idx_users_created_at`: Index on created_at for sorting/filtering

### 2. Todos Table
Stores individual todo items.

**Table Name**: `todos`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the todo |
| user_id | UUID | FOREIGN KEY, NOT NULL | Reference to the owner user |
| title | VARCHAR(255) | NOT NULL | Title of the todo |
| description | TEXT | NULL | Detailed description of the todo |
| completed | BOOLEAN | DEFAULT FALSE | Completion status |
| priority | VARCHAR(20) | DEFAULT 'medium' | Priority level (low, medium, high, urgent) |
| due_date | TIMESTAMP | NULL | Due date for the todo |
| category_id | UUID | FOREIGN KEY, NULL | Reference to category |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() ON UPDATE | Last update timestamp |

**Indexes**:
- `idx_todos_user_id`: Index on user_id for user-specific queries
- `idx_todos_completed`: Index on completed status for filtering
- `idx_todos_priority`: Index on priority for sorting
- `idx_todos_due_date`: Index on due_date for deadline filtering
- `idx_todos_category_id`: Index on category_id for category filtering

**Constraints**:
- `chk_priority`: Check constraint to ensure priority is one of ('low', 'medium', 'high', 'urgent')
- `chk_future_due_date`: Check constraint to ensure due_date is not in the past (optional)

### 3. Categories Table
Stores categories/tags for organizing todos.

**Table Name**: `categories`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the category |
| user_id | UUID | FOREIGN KEY, NOT NULL | Reference to the owner user |
| name | VARCHAR(100) | NOT NULL | Category name |
| color | VARCHAR(7) | DEFAULT '#000000' | Color code for UI representation |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() ON UPDATE | Last update timestamp |

**Indexes**:
- `idx_categories_user_id`: Index on user_id for user-specific queries
- `idx_categories_name`: Index on name for faster lookups

**Unique Constraint**:
- `uq_user_category`: Ensures unique category names per user

### 4. Refresh Tokens Table
Stores refresh tokens for authentication (if using refresh tokens).

**Table Name**: `refresh_tokens`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the token |
| user_id | UUID | FOREIGN KEY, NOT NULL | Reference to the user |
| token | VARCHAR(255) | UNIQUE, NOT NULL | Refresh token value |
| expires_at | TIMESTAMP | NOT NULL | Expiration timestamp |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| is_revoked | BOOLEAN | DEFAULT FALSE | Token revocation status |

**Indexes**:
- `idx_refresh_tokens_user_id`: Index on user_id for user-specific queries
- `idx_refresh_tokens_token`: Index on token for fast lookup
- `idx_refresh_tokens_expires_at`: Index on expires_at for cleanup

## Relationships

### Users and Todos
- **Relationship**: One-to-Many
- **Description**: A user can have many todos
- **Foreign Key**: `todos.user_id` references `users.id`
- **Cascade**: DELETE (when a user is deleted, all their todos are deleted)

### Users and Categories
- **Relationship**: One-to-Many
- **Description**: A user can have many categories
- **Foreign Key**: `categories.user_id` references `users.id`
- **Cascade**: DELETE (when a user is deleted, all their categories are deleted)

### Todos and Categories
- **Relationship**: Many-to-One
- **Description**: A todo belongs to one category (optional)
- **Foreign Key**: `todos.category_id` references `categories.id`
- **Cascade**: SET NULL (when a category is deleted, associated todos have category_id set to NULL)

## Model Definitions (SQLModel)

### User Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str
    is_active: bool = True
    email_verified: bool = False

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    todos: List["Todo"] = Relationship(back_populates="user")
    categories: List["Category"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
```

### Todo Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, date
import uuid

class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = Field(default="medium", regex="^(low|medium|high|urgent)$")
    due_date: Optional[datetime] = None
    
class Todo(TodoBase, table=True):
    __tablename__ = "todos"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    category_id: Optional[uuid.UUID] = Field(foreign_key="categories.id", ondelete="SET NULL")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: User = Relationship(back_populates="todos")
    category: Optional["Category"] = Relationship(back_populates="todos")

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    category_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
```

### Category Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class CategoryBase(SQLModel):
    name: str
    color: str = "#000000"

class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: User = Relationship(back_populates="categories")
    todos: List[Todo] = Relationship(back_populates="category")

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
```

## Migration Strategy
1. Use Alembic for database migrations
2. Generate migration scripts using SQLModel's automatic detection
3. Apply migrations in sequence during deployment
4. Maintain backward compatibility where possible

## Indexing Strategy
- Primary indexes on all primary keys (auto-generated)
- Foreign key indexes for relationship queries
- Frequently queried columns (email, user_id, completed status)
- Composite indexes for common query patterns if needed

## Data Integrity
- Use foreign key constraints to maintain referential integrity
- Implement check constraints for data validation
- Use appropriate NOT NULL constraints
- Implement soft deletes if needed for audit trails (instead of hard deletes)