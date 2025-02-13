from sqlalchemy import Column, Integer, String, JSON
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    coins = Column(Integer, default=1000)
    inventory = Column(JSON, default=[])

    coin_history = Column(JSON, default={
        "received": [],
        "sent": []
    })
