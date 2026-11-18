"""
OpenAI client implementation for AI WriteMate.
Uses the modern openai>=1.0.0 SDK.
Provides standard generation, streaming generation, and robust error handling.
"""

import os
from typing import Generator, Optional, List

try:
    from openai import OpenAI
    from openai import (
        OpenAIError,
        AuthenticationError,
        RateLimitError,
        APIConnectionError,
        BadRequestError,
    )
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


SUPPORTED_OPENAI_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
    "gpt-6-astra",
    "​gpt-6.1-solaris",

]

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


class OpenAIClient:
    """Wrapper for OpenAI API calls using the modern v1 SDK."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file "
                "or pass it directly to the client."
            )

        if not HAS_OPENAI:
            raise ImportError(
                "The 'openai' package is not installed. Please run: pip install openai>=1.0.0"
            )

        self.client = OpenAI(api_key=self.api_key)

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: str = DEFAULT_OPENAI_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """
        Generates text completion using OpenAI Chat Completions API.
        Returns the full response string.
        """
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            choice = response.choices[0]
            return choice.message.content or ""

        except Exception as exc:
            self._handle_error(exc)

    def generate_stream(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: str = DEFAULT_OPENAI_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Generator[str, None, None]:
        """
        Generates text completion in a streaming fashion.
        Yields text deltas as they arrive from OpenAI.
        """
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as exc:
            self._handle_error(exc)

    @staticmethod
    def _handle_error(exc: Exception) -> None:
        """Parses and formats OpenAI-specific errors into friendly messages."""
        if HAS_OPENAI:
            if isinstance(exc, AuthenticationError):
                raise PermissionError(
                    "OpenAI API key is invalid or expired. Please verify your OPENAI_API_KEY."
                ) from exc
            elif isinstance(exc, RateLimitError):
                raise RuntimeError(
                    "OpenAI rate limit or usage quota exceeded. Please check your billing or switch providers."
                ) from exc
            elif isinstance(exc, APIConnectionError):
                raise ConnectionError(
                    "Failed to connect to OpenAI servers. Please check your network connection."
                ) from exc
            elif isinstance(exc, BadRequestError):
                raise ValueError(f"OpenAI bad request: {exc.message}") from exc

        raise RuntimeError(f"OpenAI API Error: {str(exc)}") from exc
