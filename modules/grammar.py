"""
Grammar checking, spellcheck, and syntax improvement module for AI WriteMate.
Provides proofreading against various style guides with optional change explanations.
"""

from typing import Optional, Generator
from ai.ai_service import get_ai_service, AIResponse
from prompts.general_prompts import GENERAL_SYSTEM_INSTRUCTION, build_grammar_check_prompt
from modules.history import save_document


class GrammarModule:
    """Handles grammar analysis, proofreading, and stylistic polishing."""

    def __init__(self):
        self.ai_service = get_ai_service()

    def check_grammar(
        self,
        text: str,
        style_guide: str = "Standard Professional English",
        show_explanations: bool = True,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> AIResponse:
        """
        Proofreads text and provides a polished version plus list of corrections.
        Optionally saves results into database history.
        """
        prompt = build_grammar_check_prompt(
            text=text,
            style_guide=style_guide,
            show_explanations=show_explanations,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.2,  # Low temperature for precision
            fallback_on_error=True,
        )
        if user_id and response.text:
            save_document(
                user_id=user_id,
                title="Grammar Check & Proofread",
                content=response.text,
                module_type="grammar",
                prompt=prompt,
                model_used=response.model,
            )
        return response

    def stream_grammar_check(
        self,
        text: str,
        style_guide: str = "Standard Professional English",
        show_explanations: bool = True,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """Streams the grammar check output in real time."""
        prompt = build_grammar_check_prompt(
            text=text,
            style_guide=style_guide,
            show_explanations=show_explanations,
        )
        yield from self.ai_service.generate_stream(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.2,
        )


_grammar_module: Optional[GrammarModule] = None


def get_grammar_module() -> GrammarModule:
    global _grammar_module
    if _grammar_module is None:
        _grammar_module = GrammarModule()
    return _grammar_module
