import logging
logging.basicConfig(level=logging.DEBUG)

print("Importing modules...")

try:
    from sqlmodel import SQLModel, Field, create_engine, Session, select
    print("SQLModel imported successfully")
except Exception as e:
    print(f"SQLModel import error: {e}")
    import traceback
    traceback.print_exc()

try:
    from models import User, Todo, Category, UserCreate, UserRead, TodoCreate, TodoRead, TodoUpdate, CategoryCreate, CategoryRead
    print("Models imported successfully")
except Exception as e:
    print(f"Models import error: {e}")
    import traceback
    traceback.print_exc()

try:
    from db import get_session, create_db_and_tables
    print("DB module imported successfully")
except Exception as e:
    print(f"DB module import error: {e}")
    import traceback
    traceback.print_exc()

try:
    from routes import auth, todos, categories
    print("Routes imported successfully")
except Exception as e:
    print(f"Routes import error: {e}")
    import traceback
    traceback.print_exc()

try:
    from main import app
    print("Main app imported successfully")
    print("App type:", type(app))
except Exception as e:
    print(f"Main app import error: {e}")
    import traceback
    traceback.print_exc()

print("All imports completed.")