# Configuration for the Todo Chatbot MCP Server

# Server settings
MCP_SERVER_HOST = "0.0.0.0"
MCP_SERVER_PORT = 8001

# Database settings
DATABASE_URL = "postgresql://username:password@localhost/todoapp_neon"
DATABASE_POOL_SIZE = 20
DATABASE_ECHO = True

# Authentication settings
AUTH_JWT_SECRET = "your-super-secret-jwt-key-change-in-production"
AUTH_JWT_ALGORITHM = "HS256"
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OpenAI settings
OPENAI_API_KEY = "your-openai-api-key"
OPENAI_MODEL = "gpt-4-turbo"  # or gpt-3.5-turbo

# Application settings
APP_NAME = "Todo Chatbot MCP Server"
APP_VERSION = "1.0.0"
DEBUG = True