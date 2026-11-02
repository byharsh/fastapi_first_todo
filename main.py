from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import database_model
import pydantic_model
from config import engine, get_db

app = FastAPI()


database_model.Base.metadata.create_all(bind=engine)


@app.get("/todos")
def get_todos(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(database_model.todo).all()
    return todos


@app.post("/todos", response_model=pydantic_model.TodoResponse)
def create_todo(
    todo: pydantic_model.TodoCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_todo = database_model.todo(title=todo.title, category=todo.category)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@app.delete("/todo/{todo_id}", response_model=pydantic_model.TodoResponse)
def delete_todo(todo_id: int, db: Annotated[Session, Depends(get_db)]):
    todo = (
        db.query(database_model.todo).filter(database_model.todo.id == todo_id).first()
    )
    if todo:
        db.delete(todo)
        db.commit()
        db.refresh(todo)
        return {"message": "Todo deleted successfully"}
    else:
        return {"message": "Todo not found"}


@app.put("/todos/{todo_id}", response_model=pydantic_model.TodoResponse)
def update_todo(
    todo_id: int, todo: pydantic_model.TodoBase, db: Annotated[Session, Depends(get_db)]
):
    existing_todo = (
        db.query(database_model.todo).filter(database_model.todo.id == todo_id).first()
    )
    if existing_todo:
        existing_todo.title = todo.title
        existing_todo.category = todo.category
        db.commit()
        db.refresh(existing_todo)
        return existing_todo
    else:
        return {"message": "Todo not found"}
