from typing import Annotated, Iterator

from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.pool import QueuePool, StaticPool
from sqlmodel import Session, create_engine
from typing_extensions import Self


class DatabaseEngine:
    """Singleton class for database connection."""

    _instance = None

    def __new__(cls) -> Self:
        """Create a new instance of the class if it does not exist."""
        if cls._instance is None:
            cls._instance = super(DatabaseEngine, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
    ) -> None:
        """Initialize the class."""
        if not hasattr(self, "initialized"):
            self._engine: Engine | None = None
            self._test_engine: Engine | None = None
            self.initialized = True

    def get_engine(self) -> Engine:
        """Get or create the engine."""
        if self._engine is None:
            self._engine = create_engine(
                url="sqlite:///library_system.db",
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
            )

        return self._engine

    def get_test_engine(self) -> Engine:
        """Get or create the engine for test DB."""
        if self._test_engine is None:
            self._test_engine = create_engine(
                "sqlite://",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )

        return self._test_engine

    def get_session(self) -> Iterator[Session]:
        """Get a session."""
        engine = self.get_engine()
        with Session(engine) as session:
            yield session

    def get_test_session(self) -> Iterator[Session]:
        """Get a session for test DB."""
        engine = self.get_test_engine()
        with Session(engine) as session:
            yield session


db_engine = DatabaseEngine()


def get_db_session() -> Iterator[Session]:
    """Get the database session."""
    yield from db_engine.get_session()


def get_db_engine() -> Engine:
    """Get the database engine."""
    return db_engine.get_engine()


def get_db_test_session() -> Iterator[Session]:
    """Get the database test session."""
    yield from db_engine.get_test_session()


def get_db_test_engine() -> Engine:
    """Get the database test engine."""
    return db_engine.get_test_engine()


db_dependency = Annotated[Session, Depends(get_db_session)]
