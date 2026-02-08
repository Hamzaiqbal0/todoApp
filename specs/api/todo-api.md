# Todo Application API Specifications

## Overview
The Todo application API provides RESTful endpoints for managing todos and user authentication. Built with FastAPI, the API follows standard conventions with JSON request/response bodies.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "details": { ... }
}
```

## Endpoints

### Authentication

#### POST /auth/register
Register a new user

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "jwt_token"
  }
}
```

#### POST /auth/login
Authenticate a user

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "jwt_token"
  }
}
```

#### POST /auth/logout
Logout a user (invalidate session)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### POST /auth/refresh
Refresh authentication token

**Request Body:**
```json
{
  "refresh_token": "refresh_token"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "token": "new_jwt_token"
  }
}
```

### Todo Management

#### GET /todos
Get all todos for the authenticated user

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `status`: Filter by status (all, active, completed) - default: all
- `priority`: Filter by priority (low, medium, high, urgent) - optional
- `category`: Filter by category/tag - optional
- `search`: Search term for title/description - optional
- `sort`: Sort by (created_at, due_date, priority, title) - default: created_at
- `order`: Sort order (asc, desc) - default: desc
- `page`: Page number for pagination - default: 1
- `limit`: Items per page - default: 10

**Response:**
```json
{
  "success": true,
  "data": {
    "todos": [
      {
        "id": "uuid",
        "title": "Todo title",
        "description": "Todo description",
        "completed": false,
        "priority": "medium",
        "due_date": "2023-12-31T23:59:59Z",
        "category": "work",
        "tags": ["important", "follow-up"],
        "created_at": "2023-12-01T10:00:00Z",
        "updated_at": "2023-12-01T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

#### GET /todos/{id}
Get a specific todo by ID

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Parameters:**
- `id`: UUID of the todo

**Response:**
```json
{
  "success": true,
  "data": {
    "todo": {
      "id": "uuid",
      "title": "Todo title",
      "description": "Todo description",
      "completed": false,
      "priority": "medium",
      "due_date": "2023-12-31T23:59:59Z",
      "category": "work",
      "tags": ["important", "follow-up"],
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-01T10:00:00Z"
    }
  }
}
```

#### POST /todos
Create a new todo

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "title": "New todo title",
  "description": "Todo description",
  "priority": "medium",
  "due_date": "2023-12-31T23:59:59Z",
  "category": "work",
  "tags": ["important", "follow-up"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "todo": {
      "id": "uuid",
      "title": "New todo title",
      "description": "Todo description",
      "completed": false,
      "priority": "medium",
      "due_date": "2023-12-31T23:59:59Z",
      "category": "work",
      "tags": ["important", "follow-up"],
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-01T10:00:00Z"
    }
  }
}
```

#### PUT /todos/{id}
Update an existing todo

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Parameters:**
- `id`: UUID of the todo

**Request Body:**
```json
{
  "title": "Updated todo title",
  "description": "Updated description",
  "completed": true,
  "priority": "high",
  "due_date": "2023-12-31T23:59:59Z",
  "category": "personal",
  "tags": ["urgent", "review"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "todo": {
      "id": "uuid",
      "title": "Updated todo title",
      "description": "Updated description",
      "completed": true,
      "priority": "high",
      "due_date": "2023-12-31T23:59:59Z",
      "category": "personal",
      "tags": ["urgent", "review"],
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-02T15:30:00Z"
    }
  }
}
```

#### PATCH /todos/{id}/toggle
Toggle the completion status of a todo

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Parameters:**
- `id`: UUID of the todo

**Response:**
```json
{
  "success": true,
  "data": {
    "todo": {
      "id": "uuid",
      "title": "Todo title",
      "description": "Todo description",
      "completed": true,
      "priority": "medium",
      "due_date": "2023-12-31T23:59:59Z",
      "category": "work",
      "tags": ["important"],
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-02T16:00:00Z"
    }
  }
}
```

#### DELETE /todos/{id}
Delete a specific todo

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Parameters:**
- `id`: UUID of the todo

**Response:**
```json
{
  "success": true,
  "message": "Todo deleted successfully"
}
```

### Categories/Tags

#### GET /categories
Get all categories/tags for the authenticated user

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "categories": [
      {
        "id": "uuid",
        "name": "work",
        "color": "#3b82f6",
        "count": 15
      }
    ]
  }
}
```

#### POST /categories
Create a new category/tag

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "name": "personal",
  "color": "#ef4444"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "category": {
      "id": "uuid",
      "name": "personal",
      "color": "#ef4444",
      "count": 0
    }
  }
}
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid request body or parameters |
| 401 | Unauthorized - Missing or invalid authentication token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource does not exist |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Unexpected server error |

## Rate Limiting
- Auth endpoints: 5 requests per minute per IP
- API endpoints: 100 requests per minute per user

## Security
- All sensitive data transmitted over HTTPS
- Passwords hashed using bcrypt
- JWT tokens with expiration times
- Input validation on all endpoints
- SQL injection prevention through ORM