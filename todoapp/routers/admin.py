from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import ToDos
from database import SessionLocal
from starlette import status
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[Session, Depends(get_current_user)]

@router.get('/todos', status_code=status.HTTP_200_OK)
def get_all_todos(db: db_dependancy, user: user_dependancy):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=403, detail='Admin role required')

    return db.query(ToDos).all()

@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user:user_dependancy, db: db_dependancy, todo_id: int):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=403, detail='Admin role required')
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(ToDos).filter(ToDos.id == todo_id).delete()
    db.commit()

