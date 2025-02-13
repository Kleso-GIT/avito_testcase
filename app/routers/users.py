from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserResponse
from app.crud import create_user, get_user
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)
