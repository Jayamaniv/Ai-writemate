"""
Data models, schema definitions, and dataclasses for AI WriteMate.
Defines SQL table schemas and Python representations of database entities.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import sqlite3


# =====================================================================
# Database Table Schemas (SQLite)
# =====================================================================

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT
);
"""

CREATE_DOCUMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    module_type TEXT NOT NULL,
    prompt TEXT,
    model_used TEXT,
    word_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
"""

CREATE_USER_PREFERENCES_TABLE = """
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id INTEGER PRIMARY KEY,
    default_model TEXT DEFAULT 'gemini-2.5-flash',
    default_tone TEXT DEFAULT 'Professional',
    theme TEXT DEFAULT 'light',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
"""

SCHEMA_STATEMENTS = [
    CREATE_USERS_TABLE,
    CREATE_DOCUMENTS_TABLE,
    CREATE_USER_PREFERENCES_TABLE,
]


# =====================================================================
# Python Entity Models (Dataclasses)
# =====================================================================

@dataclass
class User:
    """Represents an application user."""
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    created_at: Optional[str] = None
    last_login: Optional[str] = None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "User":
        """Factory method to instantiate a User from an SQLite Row."""
        return cls(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
            created_at=row["created_at"],
            last_login=row["last_login"] if "last_login" in row.keys() else None,
        )

    def to_safe_dict(self) -> Dict[str, Any]:
        """Returns user data safe for session state (excluding password hash)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "last_login": self.last_login,
        }


@dataclass
class DocumentRecord:
    """Represents a saved or generated writing document."""
    id: Optional[int]
    user_id: int
    title: str
    content: str
    module_type: str
    prompt: Optional[str] = None
    model_used: Optional[str] = None
    word_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "DocumentRecord":
        """Factory method to instantiate a DocumentRecord from an SQLite Row."""
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            content=row["content"],
            module_type=row["module_type"],
            prompt=row["prompt"] if "prompt" in row.keys() else None,
            model_used=row["model_used"] if "model_used" in row.keys() else None,
            word_count=row["word_count"] if "word_count" in row.keys() else 0,
            created_at=row["created_at"],
            updated_at=row["updated_at"] if "updated_at" in row.keys() else None,
        )


@dataclass
class UserPreferences:
    """Represents personalized user preferences."""
    user_id: int
    default_model: str = "gemini-2.5-flash"
    default_tone: str = "Professional"
    theme: str = "light"
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "UserPreferences":
        return cls(
            user_id=row["user_id"],
            default_model=row["default_model"],
            default_tone=row["default_tone"],
            theme=row["theme"],
            created_at=row["created_at"] if "created_at" in row.keys() else None,
        )
