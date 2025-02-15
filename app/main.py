from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.security import HTTPBearer

from app.routers import register, auth, buy, info, sendCoin
from app.database import engine, Base
from dotenv import load_dotenv
from redis import asyncio as aioredis

load_dotenv()
security = HTTPBearer()

app = FastAPI(
    title="API Avito shop",
    version="1.0.0",
    description="API для управления монетами, инвентарем и транзакциями.",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)


app.include_router(register.router)
app.include_router(auth.router)
app.include_router(buy.router)
app.include_router(info.router)
app.include_router(sendCoin.router)

Base.metadata.create_all(bind=engine)
