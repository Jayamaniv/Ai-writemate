"""
Core writing module for AI WriteMate.
Orchestrates blog posts, emails, code explanations/reviews, and social media generation.
Integrates prompt templates, AI Service execution, streaming, and optional database persistence.
"""

from typing import Optional, List, Generator
from ai.ai_service import get_ai_service, AIResponse
from modules.history import save_document

# Prompt templates
from prompts.blog_prompts import (
    BLOG_SYSTEM_INSTRUCTION,
    build_blog_article_prompt,
    build_blog_outline_prompt,
    build_blog_title_ideas_prompt,
    build_seo_meta_prompt,
)
from prompts.email_prompts import (
    EMAIL_SYSTEM_INSTRUCTION,
    build_email_draft_prompt,
    build_cold_outreach_prompt,
    build_follow_up_email_prompt,
    build_email_reply_prompt,
)
from prompts.code_prompts import (
    CODE_SYSTEM_INSTRUCTION,
    build_code_explanation_prompt,
    build_code_review_prompt,
    build_docstring_and_comments_prompt,
    build_bug_debugging_prompt,
)
from prompts.social_prompts import (
    SOCIAL_SYSTEM_INSTRUCTION,
    build_linkedin_post_prompt,
    build_twitter_thread_prompt,
    build_instagram_caption_prompt,
    build_repurpose_content_prompt,
)


class WritingModule:
    """High-level writing assistant interface."""

    def __init__(self):
        self.ai_service = get_ai_service()

    # =================================================================
    # Blog & Long-Form Articles
    # =================================================================

    def write_blog_post(
        self,
        topic: str,
        target_audience: str = "General readers",
        tone: str = "Engaging & Informative",
        target_word_count: int = 800,
        keywords: Optional[List[str]] = None,
        outline: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        user_id: Optional[int] = None,
    ) -> AIResponse:
        """Generates a complete blog post and optionally persists to history."""
        prompt = build_blog_article_prompt(
            topic=topic,
            target_audience=target_audience,
            tone=tone,
            target_word_count=target_word_count,
            keywords=keywords,
            outline=outline,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=BLOG_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=3000,
            fallback_on_error=True,
        )
        if user_id and response.text:
            save_document(
                user_id=user_id,
                title=f"Blog: {topic[:50]}",
                content=response.text,
                module_type="blog",
                prompt=prompt,
                model_used=response.model,
            )
        return response

    def stream_blog_post(
        self,
        topic: str,
        target_audience: str = "General readers",
        tone: str = "Engaging & Informative",
        target_word_count: int = 800,
        keywords: Optional[List[str]] = None,
        outline: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Generator[str, None, None]:
        """Streams a blog post generation chunk by chunk."""
        prompt = build_blog_article_prompt(
            topic=topic,
            target_audience=target_audience,
            tone=tone,
            target_word_count=target_word_count,
            keywords=keywords,
            outline=outline,
        )
        yield from self.ai_service.generate_stream(
            prompt=prompt,
            system_instruction=BLOG_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=3000,
        )

    def generate_blog_outline(
        self,
        topic: str,
        target_audience: str = "General readers",
        tone: str = "Informative",
        num_sections: int = 5,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> AIResponse:
        """Generates a structured outline for a blog post."""
        prompt = build_blog_outline_prompt(topic, target_audience, tone, num_sections)
        return self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=BLOG_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
        )

    # =================================================================
    # Email Communications
    # =================================================================

    def write_email(
        self,
        recipient: str,
        purpose: str,
        key_points: str,
        tone: str = "Professional",
        sender_name: Optional[str] = None,
        call_to_action: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.6,
        user_id: Optional[int] = None,
    ) -> AIResponse:
        """Drafts a complete professional email."""
        prompt = build_email_draft_prompt(
            recipient=recipient,
            purpose=purpose,
            key_points=key_points,
            tone=tone,
            sender_name=sender_name,
            call_to_action=call_to_action,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=EMAIL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=temperature,
            fallback_on_error=True,
        )
        if user_id and response.text:
            save_document(
                user_id=user_id,
                title=f"Email: {purpose[:50]}",
                content=response.text,
                module_type="email",
                prompt=prompt,
                model_used=response.model,
            )
        return response

    def stream_email(
        self,
        recipient: str,
        purpose: str,
        key_points: str,
        tone: str = "Professional",
        sender_name: Optional[str] = None,
        call_to_action: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """Streams an email generation chunk by chunk."""
        prompt = build_email_draft_prompt(
            recipient=recipient,
            purpose=purpose,
            key_points=key_points,
            tone=tone,
            sender_name=sender_name,
            call_to_action=call_to_action,
        )
        yield from self.ai_service.generate_stream(
            prompt=prompt,
            system_instruction=EMAIL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
        )

    # =================================================================
    # Code Documentation & Reviews
    # =================================================================

    def explain_code(
        self,
        code_snippet: str,
        language: str = "Auto-detect",
        target_audience: str = "Junior Developer",
        provider: Optional[str] = None,
        model: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> AIResponse:
        """Explains a code snippet with architecture, complexity, and caveats."""
        prompt = build_code_explanation_prompt(code_snippet, language, target_audience)
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=CODE_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.3,
            max_tokens=2500,
            fallback_on_error=True,
        )
        if user_id and response.text:
            save_document(
                user_id=user_id,
                title=f"Code Explanation: {language}",
                content=response.text,
                module_type="code",
                prompt=prompt,
                model_used=response.model,
            )
        return response

    def stream_code_explanation(
        self,
        code_snippet: str,
        language: str = "Auto-detect",
        target_audience: str = "Junior Developer",
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """Streams a code explanation chunk by chunk."""
        prompt = build_code_explanation_prompt(code_snippet, language, target_audience)
        yield from self.ai_service.generate_stream(
            prompt=prompt,
            system_instruction=CODE_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.3,
            max_tokens=2500,
        )

    def review_code(
        self,
        code_snippet: str,
        language: str = "Auto-detect",
        focus_areas: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> AIResponse:
        """Conducts a comprehensive code review."""
        prompt = build_code_review_prompt(code_snippet, language, focus_areas)
        return self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=CODE_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.3,
            max_tokens=2500,
        )

    # =================================================================
    # Social Media Content
    # =================================================================

    def write_social_post(
        self,
        platform: str,
        topic: str,
        details: str,
        tone: str = "Engaging",
        provider: Optional[str] = None,
        model: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> AIResponse:
        """Generates platform-specific social media copy (LinkedIn, Twitter, Instagram)."""
        platform_lower = platform.lower()
        if "linkedin" in platform_lower:
            prompt = build_linkedin_post_prompt(topic, details, tone=tone)
        elif "twitter" in platform_lower or "x" in platform_lower:
            prompt = build_twitter_thread_prompt(topic, key_takeaways=details)
        elif "instagram" in platform_lower:
            prompt = build_instagram_caption_prompt(topic, visual_description=details, tone=tone)
        else:
            prompt = build_repurpose_content_prompt(details, target_platform=platform)

        response = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=SOCIAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.7,
            fallback_on_error=True,
        )
        if user_id and response.text:
            save_document(
                user_id=user_id,
                title=f"Social ({platform}): {topic[:40]}",
                content=response.text,
                module_type="social",
                prompt=prompt,
                model_used=response.model,
            )
        return response

    def stream_social_post(
        self,
        platform: str,
        topic: str,
        details: str,
        tone: str = "Engaging",
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """Streams a social post chunk by chunk."""
        platform_lower = platform.lower()
        if "linkedin" in platform_lower:
            prompt = build_linkedin_post_prompt(topic, details, tone=tone)
        elif "twitter" in platform_lower or "x" in platform_lower:
            prompt = build_twitter_thread_prompt(topic, key_takeaways=details)
        else:
            prompt = build_instagram_caption_prompt(topic, visual_description=details, tone=tone)

        yield from self.ai_service.generate_stream(
            prompt=prompt,
            system_instruction=SOCIAL_SYSTEM_INSTRUCTION,
            provider=provider,
            model=model,
            temperature=0.7,
        )


# Singleton instance helper
_writing_module_instance: Optional[WritingModule] = None


def get_writing_module() -> WritingModule:
    global _writing_module_instance
    if _writing_module_instance is None:
        _writing_module_instance = WritingModule()
    return _writing_module_instance
