from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, CoinHistory, ErrorResponse
from app.utils import get_password_hash, raise_http_exception

router = APIRouter(prefix="/api", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
    summary="Регистрация нового пользователя",
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise_http_exception(status.HTTP_400_BAD_REQUEST, "Имя пользователя уже занято")

    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            hashed_password=hashed_password,
            coins=1000
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка при регистрации пользователя")

    return {
        "id": db_user.id,
        "username": db_user.username,
        "coins": db_user.coins,
        "inventory": [],
        "coin_history": CoinHistory(received=[], sent=[])
    }
