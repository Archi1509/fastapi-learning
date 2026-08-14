from fastapi import APIRouter

router = APIRouter()

@router.post("/auth")
def auth():
    return {"authenticated": "successfully authenticated"}