# app/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from sqlalchemy.sql.functions import current_user
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.post(
    "/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new task for the current user
    """
    db_task = Task(**task.dict(), owner_id=current_user.id)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@router.get("/tasks/", response_model=List[TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all tasks for the current user with optional filters
    """
    query = db.query(Task).filter(Task.owner_id == current_user.id)

    # Apply filters
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)

    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a specific task by ID
    """
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a task
    """
    # Get task
    db_task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    # Update fields
    update_data = task_update.dict(exclude_unset=True)

    # If marking as completed, set completed_at timestamp
    if update_data.get("is_completed") and not db_task.is_completed:
        update_data["completed_at"] = datetime.utcnow()

    # If unmarking as completed, clear completed_at
    if update_data.get("is_completed") == False and db_task.is_completed:  # type: ignore
        update_data["completed_at"] = None

    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)

    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a task
    """
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return None


@router.get("/tasks/stats/summary")
def get_task_stats(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    """
    Get task statistics for current user
    """
    total = db.query(Task).filter(Task.owner_id == current_user.id).count()
    completed = (
        db.query(Task)
        .filter(Task.owner_id == current_user.id, Task.is_completed == True)
        .count()
    )
    todo = (
        db.query(Task)
        .filter(Task.owner_id == current_user.id, Task.status == TaskStatus.TODO)
        .count()
    )
    in_progress = (
        db.query(Task)
        .filter(Task.owner_id == current_user.id, Task.status == TaskStatus.IN_PROGRESS)
        .count()
    )

    return {
        "total": total,
        "commpleted": completed,
        "todo": todo,
        "in_progress": in_progress,
        "completion_rate": round(completed / total * 100, 2) if total > 0 else 0,
    }
