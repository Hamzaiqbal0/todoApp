import openai
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
from mcp.client import Client

load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class TodoAgent:
    """
    AI Agent that handles natural language processing for todo management
    and interacts with MCP tools to perform actions.
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=openai.api_key)
        self.mcp_client = None  # Will be initialized when connecting to MCP server
        
        # Define the system prompt for the AI agent
        self.system_prompt = """
        You are a helpful AI assistant that manages todo lists through natural language.
        You can help users create, update, delete, and view their todo items.
        You have access to specific tools for each operation.
        
        When a user gives you a command:
        1. Determine the intent (create, update, delete, view, etc.)
        2. Extract relevant parameters (title, description, priority, due date, etc.)
        3. Call the appropriate tool with the extracted parameters
        4. Respond to the user with the result
        
        Available tools:
        - create_todo: Create a new todo item
        - get_todos: Retrieve user's todo items
        - update_todo: Update an existing todo item
        - delete_todo: Delete a todo item
        - toggle_todo_completion: Toggle completion status of a todo
        - get_todo_stats: Get user's todo statistics
        - get_user_profile: Get user information
        
        Be helpful and conversational in your responses.
        """
    
    def connect_to_mcp(self, mcp_client: Client):
        """Connect the agent to the MCP server"""
        self.mcp_client = mcp_client
    
    def process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> str:
        """
        Process a user message and return an AI-generated response.
        
        Args:
            user_message: The natural language message from the user
            user_context: Additional context about the user (will include auth token in real implementation)
        
        Returns:
            AI-generated response to the user
        """
        try:
            # Prepare the messages for the OpenAI API
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Define the available functions (MCP tools)
            functions = [
                {
                    "name": "create_todo",
                    "description": "Create a new todo item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the todo"},
                            "description": {"type": "string", "description": "Optional description"},
                            "priority": {"type": "string", "description": "Priority level (low, medium, high, urgent)", "default": "medium"},
                            "due_date": {"type": "string", "description": "Optional due date in ISO format"},
                            "category": {"type": "string", "description": "Optional category"}
                        },
                        "required": ["title"]
                    }
                },
                {
                    "name": "get_todos",
                    "description": "Retrieve user's todo items with optional filters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status_filter": {"type": "string", "description": "Filter by status (all, active, completed)"},
                            "priority_filter": {"type": "string", "description": "Filter by priority level"},
                            "category_filter": {"type": "string", "description": "Filter by category"},
                            "limit": {"type": "integer", "description": "Maximum number of results", "default": 10},
                            "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                        }
                    }
                },
                {
                    "name": "update_todo",
                    "description": "Update an existing todo item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {"type": "string", "description": "ID of the todo to update"},
                            "title": {"type": "string", "description": "New title (optional)"},
                            "description": {"type": "string", "description": "New description (optional)"},
                            "completed": {"type": "boolean", "description": "New completion status (optional)"},
                            "priority": {"type": "string", "description": "New priority (optional)"},
                            "due_date": {"type": "string", "description": "New due date (optional)"},
                            "category": {"type": "string", "description": "New category (optional)"}
                        },
                        "required": ["todo_id"]
                    }
                },
                {
                    "name": "delete_todo",
                    "description": "Delete a todo item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {"type": "string", "description": "ID of the todo to delete"}
                        },
                        "required": ["todo_id"]
                    }
                },
                {
                    "name": "toggle_todo_completion",
                    "description": "Toggle the completion status of a todo item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {"type": "string", "description": "ID of the todo to toggle"}
                        },
                        "required": ["todo_id"]
                    }
                },
                {
                    "name": "get_todo_stats",
                    "description": "Get user's todo statistics",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "get_user_profile",
                    "description": "Get user information",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
            
            # Call the OpenAI API with function calling
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=messages,
                functions=functions,
                function_call="auto",  # Auto-determine which function to call
                temperature=0.7
            )
            
            # Get the response
            response_message = response.choices[0].message
            
            # Check if the model wants to call a function
            if response_message.function_call:
                # Execute the function call
                function_name = response_message.function_call.name
                function_args = eval(response_message.function_call.arguments)
                
                # Call the appropriate MCP tool
                result = self.call_mcp_tool(function_name, function_args)
                
                # Add the function result to the messages and get a final response
                messages.append(response_message)
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": str(result)
                })
                
                # Get the final response from the AI
                final_response = self.client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                    messages=messages,
                    temperature=0.7
                )
                
                return final_response.choices[0].message.content
            else:
                # If no function call was made, return the AI's response directly
                return response_message.content
                
        except Exception as e:
            return f"Sorry, I encountered an error processing your request: {str(e)}"
    
    def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call an MCP tool with the given arguments.
        
        Args:
            tool_name: Name of the MCP tool to call
            arguments: Arguments to pass to the tool
        
        Returns:
            Result from the MCP tool
        """
        # In a real implementation, this would call the actual MCP tool
        # For now, we'll simulate the call
        
        # This is where we would use the MCP client to call the actual tool
        # For demonstration purposes, we'll return mock responses
        if tool_name == "create_todo":
            # Simulate creating a todo
            import uuid
            from datetime import datetime
            return {
                "success": True,
                "todo": {
                    "id": str(uuid.uuid4()),
                    "title": arguments.get("title", "Untitled"),
                    "description": arguments.get("description", ""),
                    "completed": False,
                    "priority": arguments.get("priority", "medium"),
                    "due_date": arguments.get("due_date"),
                    "category": arguments.get("category"),
                    "owner_id": "user123",  # Would come from auth
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            }
        elif tool_name == "get_todos":
            # Simulate getting todos
            return {
                "success": True,
                "todos": [
                    {
                        "id": "1",
                        "title": "Sample task",
                        "description": "This is a sample task",
                        "completed": False,
                        "priority": "medium",
                        "due_date": None,
                        "category": "work",
                        "owner_id": "user123",
                        "created_at": datetime.utcnow().isoformat(),
                        "updated_at": datetime.utcnow().isoformat()
                    }
                ]
            }
        elif tool_name == "get_todo_stats":
            # Simulate getting stats
            return {
                "success": True,
                "total": 5,
                "completed": 2,
                "pending": 3,
                "overdue": 1
            }
        else:
            # For other tools, return a generic success
            return {"success": True, "result": f"Called {tool_name} with args: {arguments}"}


# Example usage
if __name__ == "__main__":
    agent = TodoAgent()
    response = agent.process_message("Add a task to buy groceries")
    print(response)