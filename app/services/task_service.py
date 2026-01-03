from fastapi import HTTPException, status
from app.models.task import Task
from app.models.user import User
from sqlalchemy.orm import Session

def create_task(db: Session, user: User, title: str, description: str, status: str = "todo"):
    task = Task(
        title=title,
        description=description,
        status=status,
        owner_id=user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(
    db: Session,
    user: User,
    limit: int = 10,
    offset: int = 0,
    status: str | None = None
):
    query = db.query(Task).filter(Task.owner_id == user.id)

    if status:
        query = query.filter(Task.status == status)

    return (
        query
        .order_by(Task.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def get_task_or_404(db: Session, task_id, user: User):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == user.id)
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

def update_task(db: Session, user: User, task_id, data):
    task = get_task_or_404(db, task_id, user)

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.status is not None:
        task.status = data.status

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, user: User, task_id):
    task = get_task_or_404(db, task_id, user)
    db.delete(task)
    db.commit()