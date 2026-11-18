"""
Core business logic, AI orchestration modules, history storage, and exporters for AI WriteMate.
"""

from modules.writing import (
    WritingModule,
    get_writing_module,
)
from modules.grammar import (
    GrammarModule,
    get_grammar_module,
)
from modules.summarizer import (
    SummarizerModule,
    get_summarizer_module,
)
from modules.rewriter import (
    RewriterModule,
    get_rewriter_module,
)
from modules.history import (
    save_document,
    get_user_documents,
    get_document_by_id,
    update_document,
    delete_document,
    get_user_history_stats,
)
from modules.exporter import (
    ExporterService,
    get_exporter_service,
)

__all__ = [
    "WritingModule",
    "get_writing_module",
    "GrammarModule",
    "get_grammar_module",
    "SummarizerModule",
    "get_summarizer_module",
    "RewriterModule",
    "get_rewriter_module",
    "save_document",
    "get_user_documents",
    "get_document_by_id",
    "update_document",
    "delete_document",
    "get_user_history_stats",
    "ExporterService",
    "get_exporter_service",
]
