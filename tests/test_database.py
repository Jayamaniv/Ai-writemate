"""
Unit tests for database connection, table schemas, and model entities in AI WriteMate.
"""

import sqlite3
import tempfile
from pathlib import Path
import pytest

from database.models import User, DocumentRecord, UserPreferences, SCHEMA_STATEMENTS
from database.db import get_connection, init_db, execute_query, fetch_one, fetch_all
import database.db as db_module


@pytest.fixture
def temp_db(monkeypatch):
    """Creates a temporary test database file."""
    temp_dir = tempfile.TemporaryDirectory()
    temp_db_path = Path(temp_dir.name) / "test_models.db"
    monkeypatch.setattr(db_module, "DB_PATH", temp_db_path)
    init_db(temp_db_path)
    yield temp_db_path
    temp_dir.cleanup()


def test_schema_initialization(temp_db):
    """Verify that all tables and constraints are created properly."""
    conn = get_connection(temp_db)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row["name"] for row in cursor.fetchall()}

    assert "users" in tables
    assert "documents" in tables
    assert "user_preferences" in tables
    conn.close()


def test_user_dataclass_mapping():
    """Verify User model factory and safe serialization."""
    user = User(
        id=42,
        username="lead_writer",
        email="lead@writemate.ai",
        password_hash="$2b$12$somehashstring",
        created_at="2026-03-15 10:00:00",
        last_login="2026-03-15 12:30:00",
    )
    safe = user.to_safe_dict()

    assert safe["id"] == 42
    assert safe["username"] == "lead_writer"
    assert safe["email"] == "lead@writemate.ai"
    assert "password_hash" not in safe


def test_document_record_dataclass_mapping():
    """Verify DocumentRecord model factory and fields."""
    doc = DocumentRecord(
        id=1,
        user_id=10,
        title="AI in 2026",
        content="Long form content body...",
        module_type="blog",
        prompt="Write a blog about AI",
        model_used="gemini-1.5-flash",
        word_count=520,
    )
    assert doc.id == 1
    assert doc.user_id == 10
    assert doc.word_count == 520
    assert doc.model_used == "gemini-1.5-flash"


def test_database_crud_helpers(temp_db):
    """Verify execute_query, fetch_one, and fetch_all helper operations."""
    # Insert user
    user_id = execute_query(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?);",
        ("test_author", "author@test.com", "hash_placeholder"),
    )
    assert user_id > 0

    # Fetch one
    row = fetch_one("SELECT * FROM users WHERE id = ?;", (user_id,))
    assert row is not None
    assert row["username"] == "test_author"

    # Insert documents
    execute_query(
        "INSERT INTO documents (user_id, title, content, module_type) VALUES (?, ?, ?, ?);",
        (user_id, "Doc 1", "Content 1", "blog"),
    )
    execute_query(
        "INSERT INTO documents (user_id, title, content, module_type) VALUES (?, ?, ?, ?)",
        (user_id, "Doc 2", "Content 2", "email"),
    )

    # Fetch all
    docs = fetch_all("SELECT * FROM documents WHERE user_id = ? ORDER BY id ASC;", (user_id,))
    assert len(docs) == 2
    assert docs[0]["title"] == "Doc 1"
    assert docs[1]["title"] == "Doc 2"
