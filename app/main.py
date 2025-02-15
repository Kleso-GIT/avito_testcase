from fastapi import FastAPI
from app.routers import register, auth, buy, info, sendCoin
from app.database import engine, Base
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(register.router)
app.include_router(auth.router)
app.include_router(buy.router)
app.include_router(info.router)
app.include_router(sendCoin.router)

Base.metadata.create_all(bind=engine)
