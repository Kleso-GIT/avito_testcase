from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, Inventory, CoinTransaction
from app.config import ITEMS
from app.schemas import ErrorResponse

router = APIRouter(prefix="/api", tags=["transactions"])


@router.get("/buy/{item}",
            responses={
                200: {"description": "Успешный ответ"},
                400: {"model": ErrorResponse, "description": "Неверный запрос"},
                401: {"model": ErrorResponse, "description": "Неавторизован"},
                500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
            },
            summary="Купить предмет за монеты",
            )
def buy_item(
        item: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    buyer = db.query(User).filter(User.id == current_user.id).first()
    if buyer is None:
        raise HTTPException(status_code=404, detail="User not found")

    if item not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")

    price = ITEMS[item]
    if buyer.coins < price:
        raise HTTPException(status_code=400, detail="Not enough coins")

    try:
        buyer.coins -= price
        db.flush()

        transaction = CoinTransaction(
            amount=price,
            sender_id=buyer.id,
            receiver_id=None,
            timestamp=datetime.utcnow()
        )
        db.add(transaction)

        item_in_inventory = db.query(Inventory).filter(
            Inventory.owner_id == buyer.id,
            Inventory.item_type == item
        ).first()

        if item_in_inventory:
            item_in_inventory.quantity += 1
        else:
            new_item = Inventory(item_type=item, quantity=1, owner_id=buyer.id)
            db.add(new_item)

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Purchase failed: {str(e)}")

    return {"message": f"Item {item} purchased successfully"}
