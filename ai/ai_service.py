"""
Unified AI Orchestration Service for AI WriteMate.
Provides a single interface for Google Gemini and OpenAI models.
Supports dynamic provider switching, automatic model detection, streaming, and error handling.
"""

import os
import time
from dataclasses import dataclass
from typing import Generator, Optional, Dict, List, Any

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

# Provider identifiers
PROVIDER_GEMINI = "gemini"
PROVIDER_OPENAI = "openai"
ALL_PROVIDERS = [PROVIDER_GEMINI, PROVIDER_OPENAI]


@dataclass
class AIResponse:
    """Standardized AI completion response."""
    text: str
    provider: str
    model: str
    latency_seconds: float
    word_count: int

    @property
    def is_empty(self) -> bool:
        return not self.text.strip()


class AIService:
    """
    Unified AI Service manager.
    Handles client initialization, model routing, fallback execution, and streaming.
    """

    def __init__(
        self,
        default_provider: str = PROVIDER_GEMINI,
        gemini_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
    ):
        self.default_provider = default_provider.lower()
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

        # Lazy-loaded clients
        self._gemini_client: Optional[GeminiClient] = None
        self._openai_client: Optional[OpenAIClient] = None

    # =================================================================
    # Client Accessors (Lazy Initialization)
    # =================================================================

    def get_gemini_client(self) -> GeminiClient:
        """Returns initialized Gemini client or raises an informative error."""
        if self._gemini_client is None:
            self.gemini_api_key = self.gemini_api_key or os.getenv("GEMINI_API_KEY")
            if not self.gemini_api_key:
                raise ValueError(
                    "Google Gemini API Key is missing. "
                    "Please add GEMINI_API_KEY to your .env file or settings."
                )
            self._gemini_client = GeminiClient(api_key=self.gemini_api_key)
        return self._gemini_client

    def get_openai_client(self) -> OpenAIClient:
        """Returns initialized OpenAI client or raises an informative error."""
        if self._openai_client is None:
            self.openai_api_key = self.openai_api_key or os.getenv("OPENAI_API_KEY")
            if not self.openai_api_key:
                raise ValueError(
                    "OpenAI API Key is missing. "
                    "Please add OPENAI_API_KEY to your .env file or settings."
                )
            self._openai_client = OpenAIClient(api_key=self.openai_api_key)
        return self._openai_client

    # =================================================================
    # Provider & Model Introspection
    # =================================================================

    def get_configured_providers(self) -> List[str]:
        """Returns list of providers that have an API key configured."""
        available = []
        if self.gemini_api_key or os.getenv("GEMINI_API_KEY"):
            available.append(PROVIDER_GEMINI)
        if self.openai_api_key or os.getenv("OPENAI_API_KEY"):
            available.append(PROVIDER_OPENAI)
        return available

    @staticmethod
    def get_supported_models() -> Dict[str, List[str]]:
        """Returns catalog of supported models grouped by provider."""
        return {
            PROVIDER_GEMINI: list(SUPPORTED_GEMINI_MODELS),
            PROVIDER_OPENAI: list(SUPPORTED_OPENAI_MODELS),
        }

    @staticmethod
    def detect_provider_from_model(model_name: str) -> str:
        """Infers the AI provider from a model name."""
        lowered = model_name.lower()
        if "gemini" in lowered:
            return PROVIDER_GEMINI
        if "gpt" in lowered or "o1" in lowered or "o3" in lowered:
            return PROVIDER_OPENAI
        # Default fallback to Gemini
        return PROVIDER_GEMINI

    def resolve_provider_and_model(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Tuple_Provider_Model:
        """Resolves provider and model defaults if not explicitly given."""
        # 1. Infer provider from model if given
        if model and not provider:
            resolved_provider = self.detect_provider_from_model(model)
        else:
            resolved_provider = (provider or self.default_provider).lower()

        # 2. Resolve default model for the chosen provider if omitted
        if not model:
            if resolved_provider == PROVIDER_GEMINI:
                resolved_model = DEFAULT_GEMINI_MODEL
            elif resolved_provider == PROVIDER_OPENAI:
                resolved_model = DEFAULT_OPENAI_MODEL
            else:
                resolved_model = DEFAULT_GEMINI_MODEL
        else:
            resolved_model = model

        return resolved_provider, resolved_model

    # =================================================================
    # Generation Operations
    # =================================================================

    def generate_text(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        fallback_on_error: bool = False,
    ) -> AIResponse:
        """
        Generates text using the chosen provider and model.
        Optionally falls back to the other provider if an error occurs.
        """
        resolved_provider, resolved_model = self.resolve_provider_and_model(provider, model)
        start_time = time.time()

        try:
            if resolved_provider == PROVIDER_GEMINI:
                client = self.get_gemini_client()
                content = client.generate(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    model=resolved_model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            elif resolved_provider == PROVIDER_OPENAI:
                client = self.get_openai_client()
                content = client.generate(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    model=resolved_model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            else:
                raise ValueError(f"Unsupported AI provider: '{resolved_provider}'")

            elapsed = round(time.time() - start_time, 2)
            word_count = len(content.split()) if content else 0

            return AIResponse(
                text=content,
                provider=resolved_provider,
                model=resolved_model,
                latency_seconds=elapsed,
                word_count=word_count,
            )

        except Exception as exc:
            # Fallback handling if enabled
            if fallback_on_error:
                fallback_provider = (
                    PROVIDER_OPENAI if resolved_provider == PROVIDER_GEMINI else PROVIDER_GEMINI
                )
                if fallback_provider in self.get_configured_providers():
                    fallback_model = (
                        DEFAULT_OPENAI_MODEL
                        if fallback_provider == PROVIDER_OPENAI
                        else DEFAULT_GEMINI_MODEL
                    )
                    return self.generate_text(
                        prompt=prompt,
                        system_instruction=system_instruction,
                        provider=fallback_provider,
                        model=fallback_model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        fallback_on_error=False,
                    )
            raise exc

    def generate_stream(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Generator[str, None, None]:
        """
        Streams generated text tokens/chunks in real time.
        Perfect for Streamlit's st.write_stream().
        """
        resolved_provider, resolved_model = self.resolve_provider_and_model(provider, model)

        if resolved_provider == PROVIDER_GEMINI:
            client = self.get_gemini_client()
            yield from client.generate_stream(
                prompt=prompt,
                system_instruction=system_instruction,
                model=resolved_model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif resolved_provider == PROVIDER_OPENAI:
            client = self.get_openai_client()
            yield from client.generate_stream(
                prompt=prompt,
                system_instruction=system_instruction,
                model=resolved_model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            raise ValueError(f"Unsupported AI provider: '{resolved_provider}'")


# Type alias for internal resolution
Tuple_Provider_Model = tuple[str, str]

# Singleton instance helper
_default_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """Returns a shared AIService singleton."""
    global _default_service
    if _default_service is None:
        _default_service = AIService()
    return _default_service
