from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import settings

async_engine = create_async_engine(
    settings.database_url,
    future=True,
    echo=True,
)

async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


def get_session():
    session = async_session()
    try:
        yield session
    finally:
        session.close()
