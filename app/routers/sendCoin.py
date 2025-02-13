from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, CoinTransaction
from app.schemas import SendCoinRequest

router = APIRouter(prefix="/api")


@router.post("/sendCoin")
def send_coin(send_request: SendCoinRequest, current_user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    if current_user.coins < send_request.amount:
        raise HTTPException(status_code=400, detail="Not enough coins")

    recipient = db.query(User).filter(User.username == send_request.toUser).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    current_user.coins -= send_request.amount

    recipient.coins += send_request.amount

    transaction = CoinTransaction(
        amount=send_request.amount,
        sender_id=current_user.id,
        receiver_id=recipient.id
    )
    db.add(transaction)

    db.commit()

    return {"message": "Coins sent successfully"}
