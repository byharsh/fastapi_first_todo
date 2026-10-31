from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str = 
    category: str = 

class TodoCreate(BaseModel):
    title: str
    is_completed: bool = False
    category: str = "General"

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[str] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    is_completed: bool 
    created_at: datetime
    category: str
    is_expired: bool

