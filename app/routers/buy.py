from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import get_current_user
from app.database import get_db
from app.models import User, Inventory, CoinTransaction
from app.config import ITEMS
from app.schemas import ErrorResponse

router = APIRouter(prefix="/api", tags=["transactions"])


@router.get(
    "/buy/{item}",
    responses={
        200: {"description": "Успешный ответ"},
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        401: {"model": ErrorResponse, "description": "Неавторизован"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
    summary="Купить предмет за монеты",
)
async def buy_item(item: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if item not in ITEMS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Предмет не найден",
        )

    price = ITEMS[item]
    if current_user.coins < price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недостаточно монет",
        )

    current_user.coins -= price
    transaction = CoinTransaction(
        amount=price,
        sender_id=current_user.id,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(transaction)

    item_in_inventory = await db.execute(select(Inventory).
                                         filter_by(owner_id=current_user.id, item_type=item))
    item_in_inventory = item_in_inventory.scalars().first()

    if item_in_inventory:
        item_in_inventory.quantity += 1
    else:
        db.add(Inventory(item_type=item, quantity=1, owner_id=current_user.id))

    await db.commit()
    return {"message": f"Предмет {item} успешно куплен"}
