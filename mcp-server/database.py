import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlmodel import create_engine as sqlmodel_create_engine

load_dotenv()

# Database configuration for Neon PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://neondb_owner:PASSWORD@ep-aged-meadow-a5q6rgwc.us-east-1.aws.neon.tech/neondb?sslmode=require"
)

# For local development with SQLite fallback
LOCAL_DATABASE_URL = os.getenv("LOCAL_DATABASE_URL", "sqlite:///./todo_chatbot.db")

def get_database_url():
    """Return the appropriate database URL based on environment"""
    # Check if we're in a production environment
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return DATABASE_URL
    else:
        return LOCAL_DATABASE_URL

# Engine configuration
def create_db_engine():
    """Create database engine with appropriate settings for Neon"""
    database_url = get_database_url()
    
    if database_url.startswith("postgresql"):
        # Configuration for Neon PostgreSQL
        return sqlmodel_create_engine(
            database_url,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=os.getenv("DATABASE_ECHO", "False").lower() == "true"
        )
    else:
        # Configuration for SQLite (fallback)
        return sqlmodel_create_engine(
            database_url,
            echo=os.getenv("DATABASE_ECHO", "False").lower() == "true"
        )

# Create the engine
engine = create_db_engine()