"""Database connection and initialization manager."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from .schema import get_schema_statements


class DatabaseManager:
    """Singleton database manager for SQLite connection."""

    _instance: Optional['DatabaseManager'] = None
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the database manager."""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.db_path: Optional[Path] = None

    def initialize(self, db_path: Path) -> None:
        """
        Initialize the database connection and create tables.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create connection
        self._connection = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=5.0
        )
        self._connection.row_factory = sqlite3.Row

        # Create tables and indexes
        self._create_schema()

    def _create_schema(self) -> None:
        """Create database tables and indexes."""
        if self._connection is None:
            raise RuntimeError("Database not initialized")

        cursor = self._connection.cursor()
        for statement in get_schema_statements():
            cursor.executescript(statement)
        self._connection.commit()

    def get_connection(self) -> sqlite3.Connection:
        """
        Get the database connection.

        Returns:
            Active SQLite connection

        Raises:
            RuntimeError: If database not initialized
        """
        if self._connection is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._connection

    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions.

        Automatically commits on success, rolls back on exception.
        """
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def close(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None


# Global singleton instance
db_manager = DatabaseManager()
