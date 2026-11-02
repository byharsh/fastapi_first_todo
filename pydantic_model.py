from datetime import datetime

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(min_length=2, max_length=100, description="Title of the todo")
    category: str = Field(
        min_length=1, max_length=35, description="Category of the todo"
    )


class TodoCreate(BaseModel):
    title: str
    is_completed: bool = False
    category: str = "General"


class TodoUpdate(BaseModel):
    title: str | None
    is_completed: bool | None = False


class TodoResponse(TodoBase):
    id: int
    title: str
    is_completed: bool
    created_at: datetime
    category: str
    is_expired: bool
