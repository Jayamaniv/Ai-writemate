"""
Google Gemini AI client implementation for AI WriteMate.
Uses exclusively the modern official google-genai SDK.
Provides standard generation, streaming generation, and robust error handling.
"""

import os
from typing import Generator, Optional, Any, List

try:
    from google import genai
    from google.genai import types as genai_types
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False


SUPPORTED_GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-pro-exp-02-05",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-3.0-flash",
    "gemini-3.0-pro",
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.8-pro",
    "gemini-4-hydrogen",
    "gemini-4-carbon",
]

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


class GeminiClient:
    """Wrapper for Google Gemini API calls using the modern google-genai SDK."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY in your .env file "
                "or pass it directly to the client."
            )

        if not HAS_GOOGLE_GENAI:
            raise ImportError(
                "The 'google-genai' package is not installed. Please run: pip install google-genai"
            )

        self.client = genai.Client(api_key=self.api_key)

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: str = DEFAULT_GEMINI_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """
        Generates text completion using Gemini.
        Returns the full response string.
        """
        try:
            config = genai_types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                system_instruction=system_instruction if system_instruction else None,
            )
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
            return response.text or ""

        except Exception as exc:
            self._handle_error(exc)

    def generate_stream(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: str = DEFAULT_GEMINI_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Generator[str, None, None]:
        """
        Generates text completion in a streaming fashion.
        Yields text chunks as they arrive from Gemini.
        """
        try:
            config = genai_types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                system_instruction=system_instruction if system_instruction else None,
            )
            stream = self.client.models.generate_content_stream(
                model=model,
                contents=prompt,
                config=config,
            )
            for chunk in stream:
                if chunk.text:
                    yield chunk.text

        except Exception as exc:
            self._handle_error(exc)

    @staticmethod
    def _handle_error(exc: Exception) -> None:
        """Parses and formats Gemini-specific errors into friendly messages."""
        error_msg = str(exc)
        if "API_KEY_INVALID" in error_msg or "401" in error_msg or "unauthenticated" in error_msg.lower():
            raise PermissionError(
                "Gemini API key is invalid or unauthorized. Please verify your GEMINI_API_KEY."
            ) from exc
        elif "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg or "quota" in error_msg.lower():
            raise RuntimeError(
                "Gemini API quota exceeded or rate limit reached. Please wait a moment or switch providers."
            ) from exc
        elif "SAFETY" in error_msg or "blocked" in error_msg.lower():
            raise ValueError(
                "Gemini content safety filters blocked the response for this prompt."
            ) from exc
        else:
            raise RuntimeError(f"Gemini API Error: {error_msg}") from exc
