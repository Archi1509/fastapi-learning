from typing import Annotated

from pydantic import BaseModel, Field

from fastapi import FastAPI, Depends, Path, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from models import ToDos
from starlette import status
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
