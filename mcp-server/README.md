# AI-Powered Todo Chatbot with MCP Server

## Overview
This project implements an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture. The system allows users to interact with their todo lists using natural language commands, with an AI agent processing these commands and performing actions via MCP tools.

## Architecture Components

### 1. MCP Server
- Implements the official MCP SDK
- Exposes todo management operations as standardized tools
- Stateless design with database-backed persistence
- Handles authentication and authorization

### 2. AI Agent
- Uses OpenAI Agent SDK
- Processes natural language input from users
- Calls appropriate MCP tools based on intent recognition
- Maintains conversation context

### 3. Database Layer
- Neon Serverless PostgreSQL for data persistence
- SQLModel ORM for database operations
- Stores todos, user data, and conversation history

### 4. Authentication
- Better Auth for secure user authentication
- JWT-based session management
- User isolation for data privacy

## Features

### Natural Language Processing
- **Creation**: "Add a task to buy groceries", "Create a todo for meeting tomorrow"
- **Retrieval**: "Show my tasks", "What are my high priority items?"
- **Updating**: "Mark task 1 as complete", "Change due date of 'project' to Friday"
- **Deletion**: "Remove the grocery task", "Delete task 2"
- **Queries**: "How many tasks do I have?", "Show overdue items"

### MCP Tools
- `create_todo` - Creates a new todo item
- `get_todos` - Retrieves user's todo items
- `update_todo` - Updates an existing todo item
- `delete_todo` - Deletes a todo item
- `toggle_todo_completion` - Toggles completion status
- `get_todo_stats` - Gets user's todo statistics
- `get_user_profile` - Retrieves user information

### User Interface
- Real-time messaging interface
- Natural language input field
- AI-generated responses with formatting
- Quick action buttons for common commands
- Visual representation of todo items

## Installation and Setup

### Prerequisites
- Python 3.9+
- PostgreSQL (or Neon Serverless PostgreSQL)
- OpenAI API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo-chatbot-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with the following:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/todoapp
   OPENAI_API_KEY=your_openai_api_key
   AUTH_JWT_SECRET=your-super-secret-jwt-key-change-in-production
   ```

4. **Initialize the database**
   ```bash
   python -c "from db import create_db_and_tables; create_db_and_tables()"
   ```

5. **Run the MCP server**
   ```bash
   python mcp_server.py
   ```

6. **Access the web interface**
   Open `chat_interface.html` in your browser

## Usage

### Starting the MCP Server
```bash
python mcp_server.py
```
The server will start on `http://localhost:8001`

### Using the Chat Interface
1. Open `chat_interface.html` in your browser
2. Authenticate using the login system
3. Type natural language commands to manage your todos
4. The AI assistant will process your requests and respond accordingly

### Example Commands
- "Add a task to buy groceries with high priority"
- "Show me all my tasks"
- "Mark task 'buy groceries' as complete"
- "Delete the task called 'old task'"
- "What are my statistics?"

## Project Structure
```
mcp-server/
├── mcp_server.py          # MCP server implementation
├── agent.py               # AI agent with OpenAI integration
├── models.py              # Database models (SQLModel)
├── db.py                  # Database connection and session management
├── database.py            # Database configuration
├── auth.py                # Authentication utilities
├── auth_better.py         # Better Auth implementation
├── chat_interface.html    # Web interface for the chatbot
├── test_system.py         # System testing script
├── requirements.txt       # Dependencies
├── config.py              # Configuration settings
└── README.md              # This file
```

## MCP Server API

The MCP server exposes the following tools:

### Todo Management Tools
- `create_todo(title, description, priority, due_date, category)`
- `get_todos(status_filter, priority_filter, category_filter, limit, offset)`
- `update_todo(todo_id, title, description, completed, priority, due_date, category)`
- `delete_todo(todo_id)`
- `toggle_todo_completion(todo_id)`
- `get_todo_stats()`
- `get_user_profile()`

## Security Considerations
- Secure API endpoints with authentication
- Input sanitization to prevent injection attacks
- Rate limiting to prevent abuse
- Data encryption for sensitive information

## Performance Requirements
- Response time under 2 seconds for typical requests
- Support for concurrent users
- Efficient database queries
- Caching for frequently accessed data

## Integration Points
- MCP server communicates with database via SQLModel
- AI agent connects to MCP tools via official SDK
- Authentication handled through Better Auth
- Frontend communicates via WebSocket or HTTP polling

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure your PostgreSQL server is running and credentials are correct
2. **OpenAI API**: Verify your API key is valid and has sufficient quota
3. **MCP Server**: Check that the server is running on the correct port

### Debugging
Enable debug mode by setting `DEBUG=true` in your environment variables.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License
This project is licensed under the MIT License.