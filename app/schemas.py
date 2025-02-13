from typing import List
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class InventoryItem(BaseModel):
    type: str
    quantity: int


class CoinTransaction(BaseModel):
    fromUser: str
    amount: int


class SentCoinTransaction(BaseModel):
    toUser: str
    amount: int


class CoinHistory(BaseModel):
    received: List[CoinTransaction]
    sent: List[SentCoinTransaction]


class UserResponse(BaseModel):
    id: int
    username: str
    coins: int
    inventory: List[InventoryItem]
    coin_history: CoinHistory

    class Config:
        from_attributes = True


class SendCoinRequest(BaseModel):
    toUser: str
    amount: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class BuyItemResponse(BaseModel):
    message: str


class SendCoinResponse(BaseModel):
    message: str


class InfoResponse(BaseModel):
    coins: int
    inventory: List[InventoryItem]
    coin_history: CoinHistory


class ErrorResponse(BaseModel):
    errors: str
