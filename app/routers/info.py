from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from ..models import User, Inventory, CoinTransaction
from ..schemas import InfoResponse, ErrorResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api", tags=["info"])


@router.get("/info", response_model=InfoResponse, responses={
    400: {"model": ErrorResponse, "description": "Неверный запрос"},
    401: {"model": ErrorResponse, "description": "Неавторизован"},
    500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
})
async def get_user_info(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        inventory_result = await db.execute(select(Inventory).filter_by(owner_id=current_user.id))
        inventory = inventory_result.scalars().all()

        sent_transactions_result = await db.execute(select(CoinTransaction).filter_by(sender_id=current_user.id))
        sent_transactions = sent_transactions_result.scalars().all()

        received_transactions_result = await db.execute(select(CoinTransaction).filter_by(receiver_id=current_user.id))
        received_transactions = received_transactions_result.scalars().all()

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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Ошибка при получении информации: {str(e)}")
