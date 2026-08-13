from typing import Annotated

from pydantic import BaseModel, Field

from fastapi import FastAPI, Depends, Path, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from models import ToDos
from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    description: str = Field(min_length=3, max_length=100)
    title: str = Field(min_length=3)
    completed: bool
    priority: int = Field(gt=0, lt=6)


@app.get("/", status_code=status.HTTP_200_OK)
def read_all(db : db_dependancy):
    return db.query(ToDos).all()

@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(db: db_dependancy, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo Not found")

@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependancy, todo_request: TodoRequest):
    todo_model = ToDos(**todo_request.dict())
    db.add(todo_model)
    db.commit()

@app.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependancy, todo_request: TodoRequest, todo_id: int= Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    todo_model.title = todo_request.title
    todo_model.completed = todo_request.completed
    todo_model.priority = todo_request.priority
    todo_model.description = todo_request.description

    db.add(todo_model)
    db.commit()

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependancy, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(ToDos).filter(ToDos.id == todo_id).delete()
    db.commit()