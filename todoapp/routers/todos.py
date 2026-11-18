from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from models import ToDos
from database import SessionLocal
from starlette import status
from .auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[Session, Depends(get_current_user)]


class TodoRequest(BaseModel):
    description: str = Field(min_length=3, max_length=100)
    title: str = Field(min_length=3)
    completed: bool
    priority: int = Field(gt=0, lt=6)


@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependancy, db : db_dependancy):
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    return db.query(ToDos).filter(ToDos.owner_id == user.get('id')).all()

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(user: user_dependancy, db: db_dependancy, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo Not found")

@router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependancy, db: db_dependancy, todo_request: TodoRequest):
    todo_model = ToDos(**todo_request.dict(), owner_id=user.get('id'))
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_dependancy, db: db_dependancy, todo_request: TodoRequest, todo_id: int= Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    todo_model.title = todo_request.title
    todo_model.completed = todo_request.completed
    todo_model.priority = todo_request.priority
    todo_model.description = todo_request.description

    db.add(todo_model)
    db.commit()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependancy, db: db_dependancy, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).delete()
    db.commit()