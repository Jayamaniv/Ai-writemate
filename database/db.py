"""
Database connection and session lifecycle management for AI WriteMate.
Handles SQLite connection pooling, foreign keys, transaction handling, and schema setup.
"""

import os
from pathlib import Path
import sqlite3
from typing import Generator, Any, Tuple, List, Optional
from contextlib import contextmanager

from database.models import SCHEMA_STATEMENTS

# Resolve database path: configurable via DATABASE_PATH env, defaults to database/writemate.db
DEFAULT_DB_PATH = Path(__file__).resolve().parent / "writemate.db"
DB_PATH = Path(os.getenv("DATABASE_PATH", str(DEFAULT_DB_PATH)))


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """
    Creates and returns a thread-safe SQLite connection.
    Enables SQLite foreign key constraints and row factory for dict-like access.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(
        str(db_path),
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_db_cursor(commit: bool = True) -> Generator[sqlite3.Cursor, None, None]:
    """
    Context manager that yields an active SQLite cursor.
    Commits transactions on success, rolls back automatically on error.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception as exc:
        conn.rollback()
        raise exc
    finally:
        cursor.close()
        conn.close()


def execute_query(sql: str, params: Tuple[Any, ...] = (), commit: bool = True) -> int:
    """Executes a write query (INSERT, UPDATE, DELETE) and returns the lastrowid or affected rows."""
    with get_db_cursor(commit=commit) as cursor:
        cursor.execute(sql, params)
        return cursor.lastrowid or cursor.rowcount


def fetch_one(sql: str, params: Tuple[Any, ...] = ()) -> Optional[sqlite3.Row]:
    """Executes a read query and returns a single row or None."""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()


def fetch_all(sql: str, params: Tuple[Any, ...] = ()) -> List[sqlite3.Row]:
    """Executes a read query and returns all matching rows."""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


def init_db(db_path: Path = DB_PATH) -> None:
    """
    Initializes the SQLite database tables if they do not exist.
    Safe to run repeatedly on application startup.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with get_db_cursor(commit=True) as cursor:
        for statement in SCHEMA_STATEMENTS:
            cleaned = statement.strip()
            if cleaned:
                cursor.execute(cleaned)


if __name__ == "__main__":
    init_db()
    print(f"Database successfully initialized at: {DB_PATH}")
