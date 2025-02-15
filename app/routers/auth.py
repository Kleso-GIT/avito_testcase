from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import (
    authenticate_user,
    create_access_token,
)

from ..database import get_db
from ..schemas import AuthResponse, ErrorResponse
from ..utils import raise_http_exception

router = APIRouter(prefix="/api", tags=["auth"])


@router.post(
    "/auth",
    response_model=AuthResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        401: {"model": ErrorResponse, "description": "Неавторизован"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
    summary="Аутентификация и получение JWT-токена",
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise_http_exception(status.HTTP_401_UNAUTHORIZED, "Неверное имя пользователя или пароль")

    access_token = create_access_token(data={"sub": user.username})
    return {"token": access_token}
