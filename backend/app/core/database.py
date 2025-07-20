"""
Database connection and session management for COGENT backend.
"""

import logging
from typing import AsyncGenerator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings

# Import models to ensure they're registered
from models import Base, User, Project, Document, SearchIndex, Usage

logger = logging.getLogger(__name__)

# Global variables for database connections
engine = None
async_engine = None
SessionLocal = None
AsyncSessionLocal = None


def get_database_url(async_mode: bool = False) -> str:
    """Get database URL with appropriate driver for sync/async operations"""
    settings = get_settings()
    db_url = settings.database_url
    
    if async_mode:
        # Convert sync URLs to async
        if db_url.startswith("sqlite:///"):
            return db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
        elif db_url.startswith("postgresql://"):
            return db_url.replace("postgresql://", "postgresql+asyncpg://")
        elif db_url.startswith("postgresql+psycopg2://"):
            return db_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    
    return db_url


def create_database_engine():
    """Create synchronous database engine"""
    global engine, SessionLocal
    
    settings = get_settings()
    db_url = get_database_url(async_mode=False)
    
    logger.info(f"Creating database engine for: {db_url.split('@')[-1] if '@' in db_url else db_url}")
    
    # Engine configuration based on database type
    if db_url.startswith("sqlite"):
        engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=settings.is_development,
        )
    else:
        # PostgreSQL configuration
        engine = create_engine(
            db_url,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_timeout=settings.db_pool_timeout,
            pool_pre_ping=True,
            echo=settings.is_development,
        )
    
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    return engine


def create_async_database_engine():
    """Create asynchronous database engine"""
    global async_engine, AsyncSessionLocal
    
    settings = get_settings()
    db_url = get_database_url(async_mode=True)
    
    logger.info(f"Creating async database engine for: {db_url.split('@')[-1] if '@' in db_url else db_url}")
    
    # Async engine configuration
    if db_url.startswith("sqlite"):
        async_engine = create_async_engine(
            db_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=settings.is_development,
        )
    else:
        # PostgreSQL async configuration
        async_engine = create_async_engine(
            db_url,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_timeout=settings.db_pool_timeout,
            pool_pre_ping=True,
            echo=settings.is_development,
        )
    
    AsyncSessionLocal = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    return async_engine


async def init_db():
    """Initialize database and create tables"""
    global engine, async_engine
    
    logger.info("Initializing database...")
    
    # Create engines
    engine = create_database_engine()
    async_engine = create_async_database_engine()
    
    # Create all tables (for development)
    # In production, this would be handled by Alembic migrations
    settings = get_settings()
    if settings.is_development:
        logger.info("Creating database tables (development mode)")
        Base.metadata.create_all(bind=engine)
    
    logger.info("Database initialization completed")


def get_db() -> Session:
    """
    FastAPI dependency to get database session.
    Use this as a dependency in your endpoints.
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get async database session.
    Use this for async endpoints if needed.
    """
    if AsyncSessionLocal is None:
        raise RuntimeError("Async database not initialized. Call init_db() first.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Async database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


def close_db_connections():
    """Close database connections (for cleanup)"""
    global engine, async_engine
    
    logger.info("Closing database connections...")
    
    if engine:
        engine.dispose()
        engine = None
    
    if async_engine:
        async_engine.dispose()
        async_engine = None
    
    logger.info("Database connections closed")