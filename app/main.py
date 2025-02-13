from fastapi import FastAPI
from app.routers import users, auth, buy, info, sendCoin
from app.database import engine, Base

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(buy.router)
app.include_router(info.router)
app.include_router(sendCoin.router)

Base.metadata.create_all(bind=engine)
