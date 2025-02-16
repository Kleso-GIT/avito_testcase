from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, Inventory, CoinTransaction
from app.schemas import InfoResponse, ErrorResponse

router = APIRouter(prefix="/api", tags=["info"])


@router.get("/info", response_model=InfoResponse, responses={
    400: {"model": ErrorResponse, "description": "Неверный запрос"},
    401: {"model": ErrorResponse, "description": "Неавторизован"},
    500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
})
def get_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        inventory = db.query(Inventory).filter_by(owner_id=current_user.id).all()
        sent_transactions = db.query(CoinTransaction).filter_by(sender_id=current_user.id).all()
        received_transactions = db.query(CoinTransaction).filter_by(receiver_id=current_user.id).all()
        return {
            "coins": current_user.coins,
            "inventory": [{"type": i.item_type, "quantity": i.quantity} for i in inventory],
            "coinHistory": {
                "received": [{"fromUser": t.sender.username if t.sender else "System", "amount": t.amount} for t in
                             received_transactions],
                "sent": [{"toUser": t.receiver.username if t.receiver else "System", "amount": t.amount} for t in
                         sent_transactions],
            },
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении информации")
