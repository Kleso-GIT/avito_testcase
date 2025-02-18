# .env
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import text
from app.config import USE_TEST_DB
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.routers import auth, buy, info, sendCoin
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if USE_TEST_DB:
        async with engine.connect() as conn:
            try:
                # Получаем список всех таблиц
                tables = Base.metadata.tables.keys()
                if tables:
                    table_names = ", ".join(f'"{t}"' for t in tables)  # Экранируем имена таблиц
                    await conn.execute(text(f'TRUNCATE {table_names} RESTART IDENTITY CASCADE'))
                    await conn.commit()  # Фиксируем изменения
                    print("Тестовая база очищена.")
            except Exception as e:
                print(f"Ошибка при очистке тестовой базы: {e}")

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
