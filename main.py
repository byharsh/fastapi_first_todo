from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import database_model
import pydantic_model
from config import engine, get_db

app = FastAPI()


database_model.Base.metadata.create_all(bind=engine)


@app.get("/todos", response_model=list[pydantic_model.TodoResponse])
def get_todos(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(database_model.todo).all()
    if not todos:
        raise HTTPException(status_code=404, detail="Not found any Todos ")
    return todos


@app.get("/todos/{todo_id}", response_model=pydantic_model.TodoResponse)
def get_todo(todo_id: int, db: Annotated[Session, Depends(get_db)]):
    db_todo = database_model.todo
    todo = db.query(db_todo).filter(db_todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


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


@app.delete("/todo/{todo_id}", response_model=pydantic_model.TodoResponseMessage)
def delete_todo(todo_id: int, db: Annotated[Session, Depends(get_db)]):
    todo = (
        db.query(database_model.todo).filter(database_model.todo.id == todo_id).first()
    )
    if todo:
        db.delete(todo)
        db.commit()
        # db.refresh(todo)
        return {"message": "Todo deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}", response_model=pydantic_model.TodoResponse)
def update_todo(
    todo_id: int,
    todo: pydantic_model.TodoUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    existing_todo = (
        db.query(database_model.todo).filter(database_model.todo.id == todo_id).first()
    )

    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        return {"message": "Todo not found"}

    new_todo = todo.model_dump(exclude_unset=True)

    for key, value in new_todo.items():
        setattr(existing_todo, key, value)

    db.commit()
    db.refresh(existing_todo)
    return existing_todo


# @app.patch("/todos/{todo_id}", response_model=pydantic_model.TodoResponse)
# def update_todo(todo_id: int,
#         todo: pydantic_model.TodoUpdate,
#         db: Annotated[Session, Depends(get_db)]):

#      existing_todo = ( db.query(database_model.todo).filter(database_model.todo.id == todo_id).first())

#      if not existing_todo:
#            # raise HTTPException(status_code=404, detail="Todo not found")
#            return {"message": "Todo not found"}

#      new_todo = todo.model_dump(exclude_unset=True)

#      for key, value in new_todo.items():
#             setattr(existing_todo, key, value)

#      db.commit()
#      db.refresh(existing_todo)
#      return existing_todo
