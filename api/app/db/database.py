from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from core.config import settings
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_async_engine(settings.ASYNC_DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

Base = declarative_base()