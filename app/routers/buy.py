from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, Inventory, CoinTransaction
from app.config import ITEMS
from app.schemas import ErrorResponse
from app.utils import raise_http_exception

router = APIRouter(prefix="/api", tags=["transactions"])


@router.get("/buy/{item}", responses={
    200: {"description": "Успешный ответ"},
    400: {"model": ErrorResponse, "description": "Неверный запрос"},
    401: {"model": ErrorResponse, "description": "Неавторизован"},
    500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
})
def buy_item(item: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if item not in ITEMS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Предмет не найден")
    price = ITEMS[item]
    if current_user.coins < price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно монет")
    current_user.coins -= price
    transaction = CoinTransaction(amount=price, sender_id=current_user.id, timestamp=datetime.utcnow())
    db.add(transaction)
    item_in_inventory = db.query(Inventory).filter_by(owner_id=current_user.id, item_type=item).first()
    if item_in_inventory:
        item_in_inventory.quantity += 1
    else:
        db.add(Inventory(item_type=item, quantity=1, owner_id=current_user.id))
    db.commit()
    return {"message": f"Предмет {item} успешно куплен"}
