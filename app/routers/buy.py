from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, Inventory
from app.config import ITEMS

router = APIRouter(prefix="/api")


@router.get("/buy/{item}")
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
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Purchase failed")

    return {"message": f"Item {item} purchased successfully"}
