from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session

from ..utils import get_password_hash

router = APIRouter(prefix="/api")


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, coins=1000, inventory=[],
                   coin_history={"received": [], "sent": []})
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
