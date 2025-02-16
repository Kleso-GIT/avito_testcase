# .env
from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI
from fastapi.security import HTTPBearer

from app.routers import auth, buy, info, sendCoin
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware


security = HTTPBearer()

app = FastAPI(
    title="API Avito shop",
    version="1.0.0",
    description="API для управления монетами, инвентарем и транзакциями.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth.router)
app.include_router(buy.router)
app.include_router(info.router)
app.include_router(sendCoin.router)
