# .env
from dotenv import load_dotenv

load_dotenv()

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.database import Base, get_db
from app.main import app
from app.config import DATABASE_URL

TEST_DATABASE_URL = DATABASE_URL + "_test"
engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def test_db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture()
def override_get_db(test_db_session):
    async def _get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def async_client(override_get_db):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        yield client
