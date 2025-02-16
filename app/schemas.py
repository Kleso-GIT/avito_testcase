from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime


class InfoResponse(BaseModel):
    coins: int
    inventory: List[dict]
    coinHistory: dict


class ErrorResponse(BaseModel):
    errors: str


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str


class SendCoinRequest(BaseModel):
    toUser: str
    amount: int = Field(gt=0, description="The amount must be greater than 0")


class CoinTransactionResponse(BaseModel):
    id: int
    amount: int
    sender_id: int
    receiver_id: None | int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class CoinHistory(BaseModel):
    received: List[CoinTransactionResponse]
    sent: List[CoinTransactionResponse]


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    coins: int
    inventory: List["InventoryItem"]
    coin_history: CoinHistory

    model_config = ConfigDict(from_attributes=True)


class InventoryItem(BaseModel):
    type: str
    quantity: int


class SendCoinResponse(BaseModel):
    message: str


class BuyItemResponse(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
