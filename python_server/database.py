"""Database configuration and helpers for the Python backend."""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models."""


DEFAULT_DATABASE_URL = "sqlite:///./python_server/app.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

# future=True enables SQLAlchemy 2.x style usage without explicit conversion
engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
)

__all__ = [
    "Base",
    "DATABASE_URL",
    "DEFAULT_DATABASE_URL",
    "SessionLocal",
    "engine",
    "init_db",
    "session_scope",
]


@contextmanager
def session_scope() -> Iterator[sessionmaker]:
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """Create all tables if they do not exist."""
    # Import models so that SQLAlchemy registers their metadata with the Base
    from . import models  # noqa: F401  pylint: disable=unused-import

    Base.metadata.create_all(bind=engine)
