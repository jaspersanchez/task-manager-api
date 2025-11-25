# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, auth, tasks  # Import the users, auth router

# FastAPI application
app = FastAPI(
    title="Task Manager API",
    description="A multi-tenant task management system",
    version="0.1.0",
)

# Configure CORS (allows frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - health check
    """
    return {"message": "Task Manager API", "status": "running", "version": "0.1.0"}


@app.get("/goodbye/{name}")
async def goodbye(name: str):
    return {"message": f"Goodbye, {name}! See you tomorrow."}


# Visit: http://127.0.0.1:8000/greet?name=John&age=25
# query parameters
@app.get("/greet")
async def greet(name: str, age: int):
    return {"message": f"Hello {name}, you are {age} years old"}


@app.get("/list")
async def get_list():
    return ["apple", "banana", "orange"]


@app.get("/number")
async def get_number():
    return 42


# Hello World endpoint
@app.get("/hello/{name}")
async def hello(name: str):
    """
    Simple hello world endpoint that greets the user by name
    """
    return {"message": f"Hello, {name}!", "endppoint": "/hello/{name}"}


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy"}
