from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models import User
from ..auth import get_current_user

router = APIRouter(prefix="/api")

ITEMS = {
    "t-shirt": 80,
    "cup": 20,
    "book": 50,
    "pen": 10,
    "powerbank": 200,
    "hoody": 300,
    "umbrella": 200,
    "socks": 10,
    "wallet": 50,
    "pink-hoody": 500
}


@router.get("/buy/{item}")
def buy_item(item: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if item not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")

    price = ITEMS[item]
    if current_user.coins < price:
        raise HTTPException(status_code=400, detail="Not enough coins")

    current_user.coins -= price

    item_in_inventory = next((i for i in current_user.inventory if i["type"] == item), None)
    if item_in_inventory:
        item_in_inventory["quantity"] += 1
    else:
        current_user.inventory.append({"type": item, "quantity": 1})

    db.commit()
    db.refresh(current_user)

    return {"message": f"Item {item} purchased successfully"}
