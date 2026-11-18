"""
Database package for AI WriteMate.
Exposes database initialization, models, and authentication services.
"""

from database.db import (
    get_connection,
    get_db_cursor,
    init_db,
    execute_query,
    fetch_one,
    fetch_all,
    DB_PATH,
)

from database.models import (
    User,
    DocumentRecord,
    UserPreferences,
    SCHEMA_STATEMENTS,
)

from database.auth import (
    hash_password,
    verify_password,
    register_user,
    authenticate_user,
    get_user_by_id,
    get_user_by_username,
    get_user_by_email,
    update_password,
)

__all__ = [
    "get_connection",
    "get_db_cursor",
    "init_db",
    "execute_query",
    "fetch_one",
    "fetch_all",
    "DB_PATH",
    "User",
    "DocumentRecord",
    "UserPreferences",
    "SCHEMA_STATEMENTS",
    "hash_password",
    "verify_password",
    "register_user",
    "authenticate_user",
    "get_user_by_id",
    "get_user_by_username",
    "get_user_by_email",
    "update_password",
]
