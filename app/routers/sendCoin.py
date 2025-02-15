from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, CoinTransaction
from app.schemas import SendCoinRequest

router = APIRouter(prefix="/api")


@router.post("/sendCoin")
def send_coin(
        send_request: SendCoinRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    sender = db.query(User).filter(User.id == current_user.id).first()
    if sender is None:
        raise HTTPException(status_code=404, detail="Sender not found")

    if sender.coins < send_request.amount:
        raise HTTPException(status_code=400, detail="Not enough coins")

    recipient = db.query(User).filter(User.username == send_request.toUser).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    print(
        f"Sender balance before: {sender.coins}, Recipient balance before: {recipient.coins}, Amount: {send_request.amount}")
    try:
        sender.coins -= send_request.amount
        recipient.coins += send_request.amount
        db.flush()

        transaction = CoinTransaction(
            amount=send_request.amount,
            sender_id=sender.id,
            receiver_id=recipient.id,
            timestamp=datetime.utcnow()
        )
        db.add(transaction)
        db.commit()

        print(
            f"Transaction successful: Sender balance after: {sender.coins}, Recipient balance after: {recipient.coins}")
    except Exception as e:
        print(f"Transaction error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

    return {"message": "Coins sent successfully"}
