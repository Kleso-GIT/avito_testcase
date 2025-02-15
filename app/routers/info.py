from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, Inventory, CoinTransaction
from app.schemas import UserResponse, InventoryItem, CoinTransactionResponse, CoinHistory, InfoResponse, ErrorResponse

router = APIRouter(prefix="/api", tags=["info"])


@router.get(
    "/info",
    response_model=InfoResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        401: {"model": ErrorResponse, "description": "Неавторизован"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
    summary="Получить информацию о монетах, инвентаре и истории транзакций",
)
def get_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.owner_id == current_user.id).all()
    inventory_items = [
        {"type": item.item_type, "quantity": item.quantity}
        for item in inventory
    ]

    sent_transactions = db.query(CoinTransaction).filter(CoinTransaction.sender_id == current_user.id).all()
    received_transactions = db.query(CoinTransaction).filter(CoinTransaction.receiver_id == current_user.id).all()

    coin_history = {
        "received": [
            {"fromUser": transaction.sender.username, "amount": transaction.amount}
            for transaction in received_transactions
        ],
        "sent": [
            {"toUser": transaction.receiver.username, "amount": transaction.amount}
            for transaction in sent_transactions
        ],
    }

    return {
        "coins": current_user.coins,
        "inventory": inventory_items,
        "coinHistory": coin_history,
    }