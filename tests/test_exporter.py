"""
Unit tests for document exports (DOCX, PDF, Markdown, Plain Text) in AI WriteMate.
"""

from modules.exporter import ExporterService


def test_markdown_export():
    """Verify Markdown export produces properly formatted header and content."""
    title = "Why AI Writes Faster"
    content = "## Introduction\n\nAI writing assistants boost speed by 5x.\n\n- Point 1\n- Point 2"

    md_output = ExporterService.export_to_markdown(title, content)
    assert f"# {title}" in md_output
    assert "Generated with AI WriteMate" in md_output
    assert "## Introduction" in md_output
    assert "- Point 1" in md_output


def test_txt_export():
    """Verify Plain Text export produces uppercase banner and clean text."""
    title = "Client Follow Up"
    content = "Hi Sarah,\n\nFollowing up on our call yesterday."

    txt_output = ExporterService.export_to_txt(title, content)
    assert title.upper() in txt_output
    assert "Date:" in txt_output
    assert content in txt_output


def test_docx_export():
    """Verify Word (.docx) export produces valid binary document bytes."""
    title = "Quarterly Business Review"
    content = """# Executive Summary
    
Revenue grew by 24% year-over-year.

## Key Wins
- Deployed AI WriteMate across 5 teams
- Reduced email response times by 40%

```python
# Deployment verification
print('All systems operational')
```
"""
    docx_bytes = ExporterService.export_to_docx(
        title=title,
        content=content,
        author="Dev Team",
        metadata={"Version": "1.0"},
    )

    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 500
    # Valid DOCX files are zip archives starting with 'PK' (0x50 0x4B 0x03 0x04)
    assert docx_bytes[:2] == b"PK"


def test_pdf_export():
    """Verify PDF export generates valid PDF binary data with standard header."""
    title = "Technical Architecture Specification"
    content = """# Overview

This document outlines the system architecture for AI WriteMate.

## Core Modules
- Database: SQLite with bcrypt
- AI Orchestration: Gemini & OpenAI
"""
    pdf_bytes = ExporterService.export_to_pdf(
        title=title,
        content=content,
        author="System Architect",
        metadata={"Status": "Approved"},
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    # Valid PDF files start with '%PDF'
    assert pdf_bytes.startswith(b"%PDF")
