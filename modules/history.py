"""
Document history and persistence manager for AI WriteMate.
Handles saving generated content to SQLite, retrieval, search, editing, and deletion.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from database.db import execute_query, fetch_one, fetch_all, get_db_cursor
from database.models import DocumentRecord


def save_document(
    user_id: int,
    title: str,
    content: str,
    module_type: str,
    prompt: Optional[str] = None,
    model_used: Optional[str] = None,
) -> int:
    """
    Saves a generated or user-edited document into the database.
    Computes word count and returns the newly inserted document ID.
    """
    clean_title = title.strip() or "Untitled Document"
    word_count = len(content.split()) if content else 0

    sql = """
    INSERT INTO documents (
        user_id, title, content, module_type, prompt, model_used, word_count, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    """
    params = (user_id, clean_title, content, module_type, prompt, model_used, word_count)
    doc_id = execute_query(sql, params, commit=True)
    return doc_id


def get_user_documents(
    user_id: int,
    limit: int = 50,
    offset: int = 0,
    module_type: Optional[str] = None,
    search_query: Optional[str] = None,
) -> List[DocumentRecord]:
    """
    Retrieves a user's document history with optional module filtering and keyword search.
    Ordered by most recently created first.
    """
    sql = "SELECT * FROM documents WHERE user_id = ?"
    params: List[Any] = [user_id]

    if module_type and module_type.lower() != "all":
        sql += " AND LOWER(module_type) = LOWER(?)"
        params.append(module_type.strip())

    if search_query and search_query.strip():
        sql += " AND (LOWER(title) LIKE LOWER(?) OR LOWER(content) LIKE LOWER(?))"
        wildcard = f"%{search_query.strip()}%"
        params.extend([wildcard, wildcard])

    sql += " ORDER BY created_at DESC LIMIT ? OFFSET ?;"
    params.extend([limit, offset])

    rows = fetch_all(sql, tuple(params))
    return [DocumentRecord.from_row(row) for row in rows]


def get_document_by_id(document_id: int, user_id: int) -> Optional[DocumentRecord]:
    """
    Retrieves a single document by ID, strictly enforcing user ownership.
    """
    sql = "SELECT * FROM documents WHERE id = ? AND user_id = ? LIMIT 1;"
    row = fetch_one(sql, (document_id, user_id))
    return DocumentRecord.from_row(row) if row else None


def update_document(
    document_id: int,
    user_id: int,
    title: str,
    content: str,
) -> bool:
    """
    Updates the title and content of an existing document.
    Re-computes word count and updates the updated_at timestamp.
    """
    clean_title = title.strip() or "Untitled Document"
    word_count = len(content.split()) if content else 0

    sql = """
    UPDATE documents
    SET title = ?, content = ?, word_count = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND user_id = ?;
    """
    affected = execute_query(sql, (clean_title, content, word_count, document_id, user_id))
    return affected > 0


def delete_document(document_id: int, user_id: int) -> bool:
    """
    Deletes a document from the database.
    Returns True if a row was deleted.
    """
    sql = "DELETE FROM documents WHERE id = ? AND user_id = ?;"
    affected = execute_query(sql, (document_id, user_id))
    return affected > 0


def get_user_history_stats(user_id: int) -> Dict[str, Any]:
    """
    Computes summary metrics for a user's writing activity:
    - total documents
    - total word count
    - top used module type
    - latest document date
    """
    total_sql = """
    SELECT 
        COUNT(*) as total_docs,
        COALESCE(SUM(word_count), 0) as total_words,
        MAX(created_at) as last_active
    FROM documents 
    WHERE user_id = ?;
    """
    row = fetch_one(total_sql, (user_id,))

    # Top module query
    top_mod_sql = """
    SELECT module_type, COUNT(*) as count 
    FROM documents 
    WHERE user_id = ? 
    GROUP BY module_type 
    ORDER BY count DESC 
    LIMIT 1;
    """
    top_row = fetch_one(top_mod_sql, (user_id,))

    return {
        "total_documents": row["total_docs"] if row else 0,
        "total_words": row["total_words"] if row else 0,
        "last_active": row["last_active"] if row else None,
        "favorite_module": top_row["module_type"] if top_row else "None yet",
    }
