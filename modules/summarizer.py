"""
Text summarization module for AI WriteMate.
Produces bullet-point summaries, executive summaries, TL;DRs, and key takeaways.
"""

from typing import Optional, Generator
from ai.ai_service import get_ai_service, AIResponse
from prompts.general_prompts import GENERAL_SYSTEM_INSTRUCTION, build_summarize_prompt
from modules.history import save_document


class SummarizerModule:
    """Handles text distillation, executive summaries, and bullet extracts."""

    def __init__(self):
        self.ai_service = get_ai_service()

    def summarize(
        self,
        text: str,
        format_type: str = "Bullet Points",
        target_length: str = "Medium (~150-250 words)",
        provider: Optional[str] = None,
        model: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> AIResponse:
        """
        Summarizes input text using the requested structure and length.
        Optionally persists to document history.
        """
        prompt = build_summarize_prompt(
            text=text,
            format_type=format_type,
            target_length=target_length,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.3,
            fallback_on_error=True,
        )
        if user_id and response.text:
            save_document(
                user_id=user_id,
                title=f"Summary: {format_type}",
                content=response.text,
                module_type="summary",
                prompt=prompt,
                model_used=response.model,
            )
        return response

    def stream_summarize(
        self,
        text: str,
        format_type: str = "Bullet Points",
        target_length: str = "Medium (~150-250 words)",
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """Streams summary generation chunk by chunk."""
        prompt = build_summarize_prompt(
            text=text,
            format_type=format_type,
            target_length=target_length,
        )
        yield from self.ai_service.generate_stream(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.3,
        )

    def generate_tldr(
        self,
        text: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> AIResponse:
        """Generates a high-impact, single-sentence TL;DR."""
        prompt = f"""
Provide a single, razor-sharp TL;DR sentence that captures the core essence of the text below.
Do not include preamble or conversational filler.

TEXT:
\"\"\"
{text}
\"\"\"
""".strip()
        return self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.2,
        )


_summarizer_module: Optional[SummarizerModule] = None


def get_summarizer_module() -> SummarizerModule:
    global _summarizer_module
    if _summarizer_module is None:
        _summarizer_module = SummarizerModule()
    return _summarizer_module
