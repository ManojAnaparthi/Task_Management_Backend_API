from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskOut(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: str

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Literal["todo", "in_progress", "done"] | None = None
