# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - health check
    """
    return {"message": "Task Manager API", "status": "running", "version": "0.1.0"}


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
