# Todo Application - Project Overview

## Project Description
The Todo Application is a full-stack web application designed to help users manage their tasks efficiently. Built with a modern technology stack, it provides a seamless experience for creating, organizing, and tracking todos with features for categorization, prioritization, and due date management.

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React or Heroicons
- **Forms**: React Hook Form with Zod validation
- **State Management**: React Context API or Zustand

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Database**: Neon PostgreSQL
- **ORM**: SQLModel (combines SQLAlchemy and Pydantic)
- **Authentication**: Better Auth (JWT-based)

### Infrastructure
- **Database Hosting**: Neon (PostgreSQL-compatible)
- **Deployment**: Docker containers
- **Environment Management**: Environment variables

## Architecture Overview

### Frontend Architecture
The frontend follows Next.js 14's App Router convention with:
- Server components by default for better performance
- Client components only when interactivity is required
- API calls centralized through `/lib/api.ts`
- Component-based architecture with reusable UI elements
- Responsive design using Tailwind CSS

### Backend Architecture
The backend is built with FastAPI providing:
- RESTful API endpoints under `/api/`
- Pydantic models for request/response validation
- SQLModel for database operations
- JWT-based authentication and authorization
- Error handling with HTTPException

## Project Structure
```
todoApp/
├── backend/                 # FastAPI server
│   ├── main.py             # Application entry point
│   ├── models.py           # SQLModel database models
│   ├── routes/             # API route handlers
│   ├── db.py               # Database connection
│   └── CLAUDE.md           # Backend guidelines
├── frontend/               # Next.js application
│   ├── app/                # Pages and layouts
│   ├── components/         # Reusable UI components
│   ├── lib/                # Utilities and API client
│   └── CLAUDE.md           # Frontend guidelines
├── specs/                  # Project specifications
│   ├── overview.md         # This file
│   ├── features/           # Feature specifications
│   ├── api/                # API specifications
│   ├── database/           # Database schema specifications
│   └── ui/                 # UI/UX specifications
├── spec-kit/               # Specification toolkit
├── docker-compose.yml      # Container orchestration
├── readme.md               # Project documentation
└── CLAUDE.md               # Project guidelines
```

## Key Features

### User Management
- User registration with email verification
- Secure login/logout functionality
- JWT-based session management
- Password reset capabilities

### Todo Management
- Create, read, update, and delete todos
- Mark todos as complete/incomplete
- Set priorities (low, medium, high, urgent)
- Assign due dates with reminder notifications
- Add descriptions and tags for organization

### Organization & Filtering
- Categorize todos with custom tags/categories
- Filter todos by status, priority, category, or due date
- Sort todos by various criteria (date, priority, title)
- Search functionality for quick todo discovery

### User Experience
- Responsive design for all device sizes
- Light and dark mode themes
- Intuitive user interface with clear navigation
- Real-time updates and smooth interactions
- Accessible design following WCAG 2.1 guidelines

## Development Workflow

### Prerequisites
- Node.js (v18 or later)
- Python (v3.9 or later)
- PostgreSQL-compatible database (Neon)
- Docker and Docker Compose (optional, for containerization)

### Setup Instructions
1. Clone the repository
2. Set up environment variables for database connection and authentication
3. Install dependencies for both frontend and backend
4. Run database migrations
5. Start both frontend and backend servers

### Running the Application
- **Frontend**: `cd frontend && npm run dev`
- **Backend**: `cd backend && uvicorn main:app --reload`
- **Both**: `docker-compose up`

## Specification-Driven Development
This project follows a specification-driven development approach where:
1. All features are documented in the `/specs` directory before implementation
2. Developers reference relevant specs before implementing features
3. Specifications are updated when requirements change
4. Implementation should align closely with the defined specifications

## API Documentation
The API follows RESTful conventions with consistent response formats. All authenticated endpoints require a JWT token in the Authorization header. Detailed endpoint specifications are available in `/specs/api/`.

## Database Schema
The application uses Neon PostgreSQL with a schema designed for efficient querying and data integrity. The schema includes tables for users, todos, categories, and authentication tokens. More details are in `/specs/database/`.

## UI/UX Guidelines
The user interface follows modern design principles with a focus on usability and accessibility. The design system specifies components, color palettes, typography, and responsive behaviors. See `/specs/ui/` for complete details.

## Future Enhancements
- Collaboration features (shared lists, assignments)
- Time tracking and productivity analytics
- Recurring todos
- Mobile application
- Email notifications
- Calendar integration