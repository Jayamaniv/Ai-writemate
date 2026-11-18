"""
Unit tests for history management and document exporters.
"""

import sqlite3
import pytest
from database.models import SCHEMA_STATEMENTS
from modules.history import (
    save_document,
    get_user_documents,
    get_document_by_id,
    update_document,
    delete_document,
    get_user_history_stats,
)
from modules.exporter import ExporterService


def test_markdown_and_txt_exporters():
    """Verify markdown and plain text exporter formatting."""
    title = "My Test Article"
    content = "This is a paragraph with **bold** text."

    md = ExporterService.export_to_markdown(title, content)
    assert f"# {title}" in md
    assert content in md

    txt = ExporterService.export_to_txt(title, content)
    assert title.upper() in txt
    assert content in txt
