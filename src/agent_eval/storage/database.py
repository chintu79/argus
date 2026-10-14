"""Database engine and session management for SQLite storage.

Framework-independent configuration with dependency injection.
SQLite foreign-key enforcement enabled explicitly.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sqlalchemy import (
    Engine,
    create_engine,
    event,
)
from sqlalchemy.orm import (
    Session,
    declarative_base,
    sessionmaker,
)

# SQLAlchemy base for persistence models
Base = declarative_base()

# Engine configuration
_DEFAULT_SQLITE_PATH = "sqlite:///./data/instance/database.sqlite"
_IN_MEMORY_SQLITE = "sqlite:///:memory:"


def create_engine_func(
    database_url: str = _DEFAULT_SQLITE_PATH,
    echo: bool = False,
) -> Engine:
    """Create a SQLAlchemy engine with SQLite-specific configuration.

    Enables foreign-key enforcement for SQLite.
    """
    engine = create_engine(database_url, echo=echo)

    # Enable SQLite foreign key enforcement
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

    return engine


def create_session_factory(
    engine: Engine,
) -> sessionmaker:
    """Create a session factory bound to the given engine."""
    return sessionmaker(bind=engine, expire_on_commit=False)


def create_session(
    session_factory: sessionmaker,
) -> Session:
    """Create a new session from the factory."""
    return session_factory()


@contextmanager
def session_scope(
    session_factory: sessionmaker,
) -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations.

    Usage:
        with session_scope(session_factory) as session:
            # do work
    """
    session = create_session(session_factory)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_sqlite_path(database_url: str) -> str:
    """Extract the file path from a SQLite URL."""
    if database_url.startswith("sqlite:///"):
        return database_url.replace("sqlite:///", "")
    elif database_url == "sqlite:///:memory:":
        return ":memory:"
    return database_url


def database_exists(database_url: str) -> bool:
    """Check if a SQLite database file exists."""
    import os

    path = get_sqlite_path(database_url)
    return path != ":memory:" and os.path.exists(path)


def initialize_database(
    engine: Engine,
    metadata: Any | None = None,
) -> None:
    """Create all tables defined on the Base metadata.

    For development and testing use only.
    In production, use Alembic migrations.
    """
    if metadata is None:
        metadata = Base.metadata
    metadata.create_all(engine)
