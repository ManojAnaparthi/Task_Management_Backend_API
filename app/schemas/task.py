from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, example="Complete project documentation")
    description: Optional[str] = Field(None, max_length=1000, example="Write comprehensive README and API documentation")
    status: Literal["todo", "in_progress", "done"] = Field(default="todo", example="todo")

class TaskOut(BaseModel):
    id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    title: str = Field(..., example="Complete project documentation")
    description: Optional[str] = Field(None, example="Write comprehensive README and API documentation")
    status: str = Field(..., example="todo")

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200, example="Updated task title")
    description: str | None = Field(None, max_length=1000, example="Updated task description")
    status: Literal["todo", "in_progress", "done"] | None = Field(None, example="in_progress")
