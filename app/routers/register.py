from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, CoinHistory
from app.utils import get_password_hash

router = APIRouter(prefix="/api")


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        coins=1000
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "id": db_user.id,
        "username": db_user.username,
        "coins": db_user.coins,
        "inventory": [],
        "coin_history": CoinHistory(received=[], sent=[])
    }
