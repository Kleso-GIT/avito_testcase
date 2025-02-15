from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from app.routers import register, auth, buy, info, sendCoin
from app.database import engine, Base
from dotenv import load_dotenv
from redis import asyncio as aioredis

load_dotenv()

app = FastAPI()


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
