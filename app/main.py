# .env
from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.routers import auth, buy, info, sendCoin
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="API Avito shop",
    version="1.0.0",
    description="API для управления монетами, инвентарем и транзакциями.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(buy.router)
app.include_router(info.router)
app.include_router(sendCoin.router)
