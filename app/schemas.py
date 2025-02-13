from pydantic import BaseModel
from typing import List


# ## ITEMS ## #

class InventoryItem(BaseModel):
    type: str
    quantity: int


# ## COINS ## #

class CoinTransaction(BaseModel):
    fromUser: str
    amount: int


class SentCoinTransaction(BaseModel):
    toUser: str
    amount: int


class CoinHistory(BaseModel):
    received: List[CoinTransaction]
    sent: List[SentCoinTransaction]


# ## USERS ## #

class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    coins: int
    inventory: List[InventoryItem]
    coin_history: CoinHistory

    class Config:
        from_attributes = True


# ## TOKENS ## #


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
