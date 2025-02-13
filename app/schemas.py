from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    coins: int
    inventory: List["InventoryItem"]

    class Config:
        from_attributes = True


class InventoryItem(BaseModel):
    type: str
    quantity: int


class CoinTransactionResponse(BaseModel):
    id: int
    amount: int
    sender_id: int
    receiver_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class CoinHistory(BaseModel):
    received: List[CoinTransactionResponse]
    sent: List[CoinTransactionResponse]


class SendCoinRequest(BaseModel):
    toUser: str
    amount: int


class SendCoinResponse(BaseModel):
    message: str


class BuyItemResponse(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class ErrorResponse(BaseModel):
    errors: str
