from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.dependencies import get_current_user, get_db
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.task_service import create_task, get_tasks, update_task, delete_task
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut)
def create(
    data: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return create_task(db, user, data.title, data.description)

@router.get("", response_model=List[TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return get_tasks(db, user)

@router.put("/{task_id}", response_model=TaskOut)
def update(
    task_id: UUID,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return update_task(db, user, task_id, data)

@router.delete("/{task_id}", status_code=204)
def delete(
    task_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    delete_task(db, user, task_id)