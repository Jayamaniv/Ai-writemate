"""
AI Service package for AI WriteMate.
Provides LLM orchestration across Google Gemini and OpenAI.
"""

from ai.gemini_client import (
    GeminiClient,
    SUPPORTED_GEMINI_MODELS,
    DEFAULT_GEMINI_MODEL,
)
from ai.openai_client import (
    OpenAIClient,
    SUPPORTED_OPENAI_MODELS,
    DEFAULT_OPENAI_MODEL,
)
from ai.ai_service import (
    AIService,
    AIResponse,
    get_ai_service,
    PROVIDER_GEMINI,
    PROVIDER_OPENAI,
    ALL_PROVIDERS,
)

__all__ = [
    "GeminiClient",
    "SUPPORTED_GEMINI_MODELS",
    "DEFAULT_GEMINI_MODEL",
    "OpenAIClient",
    "SUPPORTED_OPENAI_MODELS",
    "DEFAULT_OPENAI_MODEL",
    "AIService",
    "AIResponse",
    "get_ai_service",
    "PROVIDER_GEMINI",
    "PROVIDER_OPENAI",
    "ALL_PROVIDERS",
]
