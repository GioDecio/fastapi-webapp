from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = (
    "sqlite+aiosqlite:///./blog.db"  # .db file is created automatically
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)  # Factory that creates a db sesssion.
# autocommit=False, autoflush=False: controls when changes are commited


class Base(DeclarativeBase):
    pass


# Session is not created in each route, it is injected
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session  # This makes the session work as a context manager
