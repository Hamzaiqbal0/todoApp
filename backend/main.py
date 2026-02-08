from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from routes import auth, todos, categories
import db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    db.create_db_and_tables()
    yield

app = FastAPI(
    title="Todo Application API",
    description="RESTful API for the Todo Application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["authentication"])
app.include_router(todos.router, prefix="/api", tags=["todos"])
app.include_router(categories.router, prefix="/api", tags=["categories"])

@app.get("/")
def read_root():
    return {"message": "Todo Application API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running smoothly"}