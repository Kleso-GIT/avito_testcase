from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, CoinTransaction
from app.schemas import SendCoinRequest, ErrorResponse
from app.utils import raise_http_exception

router = APIRouter(prefix="/api", tags=["transactions"])


@router.post(
    "/sendCoin",
    responses={
        200: {"description": "Успешный ответ"},
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        401: {"model": ErrorResponse, "description": "Неавторизован"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
    summary="Отправить монеты другому пользователю",
)
def send_coin(
        send_request: SendCoinRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if current_user.coins < send_request.amount:
        raise_http_exception(status.HTTP_400_BAD_REQUEST, "Недостаточно монет")

    recipient = db.query(User).filter(User.username == send_request.toUser).first()
    if not recipient:
        raise_http_exception(status.HTTP_400_BAD_REQUEST, "Получатель не найден")

    if current_user.username == send_request.toUser:
        raise_http_exception(status.HTTP_400_BAD_REQUEST, "Нельзя отправить монеты самому себе")

    try:
        current_user.coins -= send_request.amount
        recipient.coins += send_request.amount
        db.flush()

        transaction = CoinTransaction(
            amount=send_request.amount,
            sender_id=current_user.id,
            receiver_id=recipient.id,
            timestamp=datetime.utcnow()
        )
        db.add(transaction)
        db.commit()
    except Exception as e:
        db.rollback()
        raise_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка при отправке монет")

    return {"message": "Монеты успешно отправлены"}
