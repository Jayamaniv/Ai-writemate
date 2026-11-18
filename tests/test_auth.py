"""
Unit tests for authentication, password hashing, and input validation in AI WriteMate.
Uses an isolated temporary database to prevent state leakage.
"""

import os
import tempfile
from pathlib import Path
import pytest

from database.models import SCHEMA_STATEMENTS
from database.db import get_connection
import database.db as db_module
from database.auth import (
    hash_password,
    verify_password,
    validate_registration_input,
    register_user,
    authenticate_user,
    get_user_by_username,
    get_user_by_email,
    update_password,
)


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    """Sets up an isolated temporary SQLite database for each test."""
    temp_dir = tempfile.TemporaryDirectory()
    temp_db_path = Path(temp_dir.name) / "test_auth.db"
    
    # Point db module to test database
    monkeypatch.setattr(db_module, "DB_PATH", temp_db_path)

    # Initialize tables
    conn = get_connection(temp_db_path)
    cursor = conn.cursor()
    for stmt in SCHEMA_STATEMENTS:
        cursor.execute(stmt)
    conn.commit()
    conn.close()

    yield temp_db_path
    temp_dir.cleanup()


def test_password_hashing():
    """Verify that bcrypt generates salted hashes and verifies accurately."""
    raw_pwd = "SecretPassword123!"
    hashed = hash_password(raw_pwd)

    assert hashed != raw_pwd
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False
    assert verify_password("", hashed) is False


def test_validate_registration_input():
    """Verify username, email, and password format validation."""
    # Valid credentials
    is_valid, _ = validate_registration_input("valid_user", "user@example.com", "secure123")
    assert is_valid is True

    # Too short username
    is_valid, msg = validate_registration_input("ab", "user@example.com", "secure123")
    assert is_valid is False
    assert "between 3 and 30" in msg

    # Invalid characters in username
    is_valid, msg = validate_registration_input("user space!", "user@example.com", "secure123")
    assert is_valid is False

    # Invalid email format
    is_valid, msg = validate_registration_input("valid_user", "not-an-email", "secure123")
    assert is_valid is False
    assert "valid email" in msg

    # Short password
    is_valid, msg = validate_registration_input("valid_user", "user@example.com", "123")
    assert is_valid is False
    assert "at least 6 characters" in msg


def test_user_registration_and_authentication():
    """Verify end-to-end user registration and authentication lifecycle."""
    # 1. Register user
    success, msg, user = register_user("writer_bob", "bob@example.com", "password123")
    assert success is True
    assert user is not None
    assert user.username == "writer_bob"
    assert user.email == "bob@example.com"
    assert user.id is not None

    # 2. Duplicate username registration fails
    dup_uname_ok, dup_msg, _ = register_user("writer_bob", "different@example.com", "password123")
    assert dup_uname_ok is False
    assert "already taken" in dup_msg

    # 3. Duplicate email registration fails
    dup_email_ok, dup_email_msg, _ = register_user("different_user", "bob@example.com", "password123")
    assert dup_email_ok is False
    assert "already exists" in dup_email_msg

    # 4. Authenticate with username
    auth_ok, _, auth_user = authenticate_user("writer_bob", "password123")
    assert auth_ok is True
    assert auth_user.id == user.id

    # 5. Authenticate with email
    auth_email_ok, _, auth_user2 = authenticate_user("bob@example.com", "password123")
    assert auth_email_ok is True
    assert auth_user2.id == user.id

    # 6. Wrong password fails
    fail_ok, fail_msg, _ = authenticate_user("writer_bob", "WrongPass999")
    assert fail_ok is False
    assert "Invalid" in fail_msg


def test_update_password():
    """Verify password update with current password verification."""
    _, _, user = register_user("password_changer", "change@example.com", "OldPassword123")
    
    # Incorrect old password fails
    updated, msg = update_password(user.id, "WrongOldPassword", "NewPassword123")
    assert updated is False
    assert "Current password does not match" in msg

    # Correct old password succeeds
    updated, msg = update_password(user.id, "OldPassword123", "NewPassword123")
    assert updated is True

    # Authenticate with new password succeeds
    auth_ok, _, _ = authenticate_user("password_changer", "NewPassword123")
    assert auth_ok is True

    # Authenticate with old password fails
    old_auth_ok, _, _ = authenticate_user("password_changer", "OldPassword123")
    assert old_auth_ok is False
