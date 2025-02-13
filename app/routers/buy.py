from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User, Inventory
from app.config import ITEMS

router = APIRouter(prefix="/api")


@router.get("/buy/{item}")
def buy_item(item: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if item not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")

    price = ITEMS[item]
    if current_user.coins < price:
        raise HTTPException(status_code=400, detail="Not enough coins")

    current_user.coins -= price

    item_in_inventory = db.query(Inventory).filter(
        Inventory.owner_id == current_user.id,
        Inventory.item_type == item
    ).first()

    if item_in_inventory:
        item_in_inventory.quantity += 1
    else:
        new_item = Inventory(item_type=item, quantity=1, owner_id=current_user.id)
        db.add(new_item)

    db.commit()

    return {"message": f"Item {item} purchased successfully"}
