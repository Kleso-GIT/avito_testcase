from .config import DATABASE_URL, TEST_DATABASE_URL, USE_TEST_DB

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

if USE_TEST_DB:
    database_url = TEST_DATABASE_URL
else:
    database_url = DATABASE_URL

engine = create_async_engine(database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
