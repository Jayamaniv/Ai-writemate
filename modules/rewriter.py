"""
Content rewriting, paraphrasing, tone adjusting, and simplification module for AI WriteMate.
Allows users to rework existing copy across diverse formats and reading levels.
"""

from typing import Optional, Generator
from ai.ai_service import get_ai_service, AIResponse
from prompts.general_prompts import (
    GENERAL_SYSTEM_INSTRUCTION,
    build_paraphrase_prompt,
    build_tone_adjustment_prompt,
    build_simplify_text_prompt,
)
from modules.history import save_document


class RewriterModule:
    """Handles paraphrasing, tone shifting, and readability simplification."""

    def __init__(self):
        self.ai_service = get_ai_service()

    # =================================================================
    # Paraphrasing
    # =================================================================

    def paraphrase(
        self,
        text: str,
        goal: str = "Enhance clarity, vocabulary, and flow",
        tone: str = "Natural",
        num_variants: int = 3,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> AIResponse:
        """Generates multiple paraphrased alternatives of an input text."""
        prompt = build_paraphrase_prompt(
            text=text,
            goal=goal,
            tone=tone,
            num_variants=num_variants,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.7,
            fallback_on_error=True,
        )
        if user_id and response.text:
            save_document(
                user_id=user_id,
                title=f"Paraphrase: {goal[:40]}",
                content=response.text,
                module_type="rewrite",
                prompt=prompt,
                model_used=response.model,
            )
        return response

    def stream_paraphrase(
        self,
        text: str,
        goal: str = "Enhance clarity, vocabulary, and flow",
        tone: str = "Natural",
        num_variants: int = 3,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """Streams paraphrased variations."""
        prompt = build_paraphrase_prompt(text=text, goal=goal, tone=tone, num_variants=num_variants)
        yield from self.ai_service.generate_stream(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.7,
        )

    # =================================================================
    # Tone Adjustment
    # =================================================================

    def adjust_tone(
        self,
        text: str,
        target_tone: str = "Professional",
        context: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> AIResponse:
        """Rewrites text to adopt a specific tone (e.g., Empathetic, Executive, Casual)."""
        prompt = build_tone_adjustment_prompt(
            text=text,
            target_tone=target_tone,
            context=context,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.6,
            fallback_on_error=True,
        )
        if user_id and response.text:
            save_document(
                user_id=user_id,
                title=f"Tone Shift: {target_tone}",
                content=response.text,
                module_type="tone_adjust",
                prompt=prompt,
                model_used=response.model,
            )
        return response

    def stream_tone_adjustment(
        self,
        text: str,
        target_tone: str = "Professional",
        context: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """Streams tone adjusted output."""
        prompt = build_tone_adjustment_prompt(text=text, target_tone=target_tone, context=context)
        yield from self.ai_service.generate_stream(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.6,
        )

    # =================================================================
    # Simplification & Plain English
    # =================================================================

    def simplify(
        self,
        text: str,
        target_reading_level: str = "Plain English (8th-grade level)",
        provider: Optional[str] = None,
        model: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> AIResponse:
        """Removes jargon and complex structures for accessible reading."""
        prompt = build_simplify_text_prompt(
            text=text,
            target_reading_level=target_reading_level,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.4,
            fallback_on_error=True,
        )
        if user_id and response.text:
            save_document(
                user_id=user_id,
                title=f"Simplified: {target_reading_level[:30]}",
                content=response.text,
                module_type="simplify",
                prompt=prompt,
                model_used=response.model,
            )
        return response


_rewriter_module: Optional[RewriterModule] = None


def get_rewriter_module() -> RewriterModule:
    global _rewriter_module
    if _rewriter_module is None:
        _rewriter_module = RewriterModule()
    return _rewriter_module
