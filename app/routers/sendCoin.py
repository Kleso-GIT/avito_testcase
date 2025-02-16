from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from ..models import User, CoinTransaction
from ..schemas import SendCoinRequest, ErrorResponse
from ..auth import get_current_user

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
async def send_coin(
        send_request: SendCoinRequest,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    if current_user.coins < send_request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недостаточно монет",
        )

    recipient = await db.execute(select(User).filter(User.username == send_request.toUser))
    recipient = recipient.scalars().first()

    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Получатель не найден",
        )

    if current_user.username == send_request.toUser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя отправить монеты самому себе",
        )

    try:
        current_user.coins -= send_request.amount
        recipient.coins += send_request.amount

        transaction = CoinTransaction(
            amount=send_request.amount,
            sender_id=current_user.id,
            receiver_id=recipient.id,
            timestamp=datetime.now(timezone.utc),
        )
        db.add(transaction)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при отправке монет: {str(e)}",
        )

    return {"message": "Монеты успешно отправлены"}
