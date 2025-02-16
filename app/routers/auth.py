from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth import authenticate_user, create_access_token
from ..database import get_db
from ..schemas import AuthResponse, ErrorResponse, UserCreate, UserResponse, CoinHistory
from ..crud import create_user, get_user

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/auth", response_model=AuthResponse, responses={
    400: {"model": ErrorResponse, "description": "Неверный запрос"},
    401: {"model": ErrorResponse, "description": "Неавторизован"},
    500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
})
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
    return {"token": create_access_token(data={"sub": user.username})}


@router.post(
    "/register",
    response_model=UserResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
    summary="Регистрация нового пользователя",
)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Имя пользователя уже занято")

    try:
        db_user = await create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при регистрации пользователя")

    return {
        "id": db_user.id,
        "username": db_user.username,
        "coins": db_user.coins,
        "inventory": [],
        "coin_history": CoinHistory(received=[], sent=[])
    }
