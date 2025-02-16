from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    coins = Column(Integer, default=1000)

    inventory = relationship("Inventory", back_populates="owner")
    sent_transactions = relationship("CoinTransaction", foreign_keys="CoinTransaction.sender_id",
                                     back_populates="sender")
    received_transactions = relationship("CoinTransaction", foreign_keys="CoinTransaction.receiver_id",
                                         back_populates="receiver")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String, index=True)
    quantity = Column(Integer, default=1)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="inventory")


class CoinTransaction(Base):
    __tablename__ = "coin_transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")
