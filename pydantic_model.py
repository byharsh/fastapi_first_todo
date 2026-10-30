from pydantic import BaseModel


class todo_create(BaseModel):
    title: str
    is_completed: bool = False
    category: str = "General"
