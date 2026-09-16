import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings
from app.models.schema import Base

logger = logging.getLogger("lenny_assistant.database")

# Handle SQLite async prefix vs PostgreSQL async prefix
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    database_url,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def init_db():
    """Initialize database tables"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        # Fallback to local SQLite if PostgreSQL connection fails
        if "sqlite" not in settings.DATABASE_URL:
            logger.warning("Attempting fallback to local SQLite database...")
            fallback_engine = create_async_engine("sqlite+aiosqlite:///./lenny_assistant.db")
            async with fallback_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Fallback SQLite database initialized successfully.")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting DB session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
