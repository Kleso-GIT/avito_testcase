from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, Inventory, CoinTransaction
from app.schemas import UserResponse, InventoryItem, CoinTransactionResponse

router = APIRouter(prefix="/api")


@router.get("/info", response_model=UserResponse)
def get_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.owner_id == current_user.id).all()
    inventory_items = [
        InventoryItem(type=item.item_type, quantity=item.quantity)
        for item in inventory
    ]

    # Получаем историю транзакций
    sent_transactions = db.query(CoinTransaction).filter(CoinTransaction.sender_id == current_user.id).all()
    received_transactions = db.query(CoinTransaction).filter(CoinTransaction.receiver_id == current_user.id).all()

    return {
        "id": current_user.id,
        "username": current_user.username,
        "coins": current_user.coins,
        "inventory": inventory_items
    }
