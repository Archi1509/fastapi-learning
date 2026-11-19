from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from models import Users
from database import SessionLocal
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/users',
    tags=['users'],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[Session, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UpdatePasswordRequest(BaseModel):
    password: str
    new_password: str

@router.get('/user', status_code=status.HTTP_200_OK)
def get_user(db:db_dependancy, user: user_dependancy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    return db.query(Users).filter(Users.id == user.get('user_id')).first()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
def update_current_user_password(db: db_dependancy, user: user_dependancy, password_request: UpdatePasswordRequest):
    if user is None:
        raise HTTPException(status_code=401)

    current_user = db.query(Users).filter( Users.id == user.get('user_id')).first()

    if not bcrypt_context.verify(password_request.password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect current password')

    current_user.hashed_password = bcrypt_context.hash(password_request.new_password)

    db.add(current_user)
    db.commit()
