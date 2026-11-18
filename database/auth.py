"""
Authentication and security service for AI WriteMate.
Handles password hashing via bcrypt, user registration, authentication, and user lookups.
"""

import re
import datetime
from typing import Optional, Tuple
import bcrypt

from database.db import fetch_one, execute_query, get_db_cursor
from database.models import User

# Email validation regex pattern
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


# =====================================================================
# Password Hashing Helpers (bcrypt)
# =====================================================================

def hash_password(plain_password: str) -> str:
    """
    Hashes a plain text password using bcrypt with a generated salt.
    Returns the hashed password decoded as a UTF-8 string for database storage.
    """
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a stored bcrypt hash.
    Safe against timing attacks.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


# =====================================================================
# Input Validation Helpers
# =====================================================================

def validate_registration_input(username: str, email: str, password: str) -> Tuple[bool, str]:
    """Validates user registration credentials."""
    username = username.strip()
    email = email.strip()

    if len(username) < 3 or len(username) > 30:
        return False, "Username must be between 3 and 30 characters."

    if not re.match(r"^[a-zA-Z0-9_.-]+$", username):
        return False, "Username can only contain letters, numbers, underscores, and dashes."

    if not EMAIL_REGEX.match(email):
        return False, "Please enter a valid email address."

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    return True, "Valid"


# =====================================================================
# User Lookup Operations
# =====================================================================

def get_user_by_id(user_id: int) -> Optional[User]:
    """Retrieves a User instance by primary key ID."""
    query = "SELECT * FROM users WHERE id = ? LIMIT 1;"
    row = fetch_one(query, (user_id,))
    return User.from_row(row) if row else None


def get_user_by_username(username: str) -> Optional[User]:
    """Retrieves a User instance by username (case-insensitive)."""
    query = "SELECT * FROM users WHERE LOWER(username) = LOWER(?) LIMIT 1;"
    row = fetch_one(query, (username.strip(),))
    return User.from_row(row) if row else None


def get_user_by_email(email: str) -> Optional[User]:
    """Retrieves a User instance by email (case-insensitive)."""
    query = "SELECT * FROM users WHERE LOWER(email) = LOWER(?) LIMIT 1;"
    row = fetch_one(query, (email.strip(),))
    return User.from_row(row) if row else None


# =====================================================================
# Authentication & Registration Operations
# =====================================================================

def register_user(
    username: str,
    email: str,
    password: str
) -> Tuple[bool, str, Optional[User]]:
    """
    Registers a new user in the database.
    
    1. Validates input formatting.
    2. Checks for existing username or email duplicates.
    3. Hashes password using bcrypt.
    4. Inserts user record and initializes default user preferences.
    
    Returns:
        Tuple of (success_status, message, created_user_or_None)
    """
    username = username.strip()
    email = email.strip().lower()

    # 1. Validate inputs
    is_valid, validation_msg = validate_registration_input(username, email, password)
    if not is_valid:
        return False, validation_msg, None

    # 2. Check uniqueness
    if get_user_by_username(username):
        return False, "Username is already taken. Please choose another.", None

    if get_user_by_email(email):
        return False, "An account with this email already exists.", None

    # 3. Hash password
    hashed_pwd = hash_password(password)

    # 4. Insert user and preferences inside a single atomic transaction
    try:
        with get_db_cursor(commit=True) as cursor:
            insert_user_sql = """
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP);
            """
            cursor.execute(insert_user_sql, (username, email, hashed_pwd))
            user_id = cursor.lastrowid

            insert_pref_sql = """
            INSERT INTO user_preferences (user_id)
            VALUES (?);
            """
            cursor.execute(insert_pref_sql, (user_id,))

        user = get_user_by_id(user_id)
        return True, "Account created successfully!", user

    except Exception as exc:
        return False, f"Registration failed due to a database error: {str(exc)}", None


def authenticate_user(
    username_or_email: str,
    password: str
) -> Tuple[bool, str, Optional[User]]:
    """
    Authenticates a user by username or email and password.
    
    1. Looks up the user account.
    2. Verifies the password using bcrypt.
    3. Updates the user's last_login timestamp upon success.
    
    Returns:
        Tuple of (success_status, message, authenticated_user_or_None)
    """
    identifier = username_or_email.strip()
    if not identifier or not password:
        return False, "Please provide both credentials.", None

    # Look up by email or username
    user = get_user_by_email(identifier) if "@" in identifier else get_user_by_username(identifier)
    if not user:
        return False, "Invalid username/email or password.", None

    # Verify password hash
    if not verify_password(password, user.password_hash):
        return False, "Invalid username/email or password.", None

    # Update last login timestamp
    try:
        now_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        execute_query(
            "UPDATE users SET last_login = ? WHERE id = ?;",
            (now_time, user.id)
        )
        user.last_login = now_time
    except Exception:
        # Non-critical update failure
        pass

    return True, "Login successful!", user


def update_password(user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
    """Updates a user's password after verifying the old password."""
    user = get_user_by_id(user_id)
    if not user:
        return False, "User not found."

    if not verify_password(old_password, user.password_hash):
        return False, "Current password does not match."

    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long."

    new_hash = hash_password(new_password)
    execute_query("UPDATE users SET password_hash = ? WHERE id = ?;", (new_hash, user_id))
    return True, "Password updated successfully."
