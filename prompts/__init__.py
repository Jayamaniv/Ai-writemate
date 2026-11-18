"""
Prompt engineering and template library for AI WriteMate.
Exposes modular prompt builders and expert system personas for blogs, emails, code, social media, and general utilities.
"""

# System instructions
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
    build_apology_or_customer_service_prompt,
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

from prompts.general_prompts import (
    GENERAL_SYSTEM_INSTRUCTION,
    build_grammar_check_prompt,
    build_summarize_prompt,
    build_paraphrase_prompt,
    build_tone_adjustment_prompt,
    build_simplify_text_prompt,
)

__all__ = [
    # System Instructions
    "BLOG_SYSTEM_INSTRUCTION",
    "EMAIL_SYSTEM_INSTRUCTION",
    "CODE_SYSTEM_INSTRUCTION",
    "SOCIAL_SYSTEM_INSTRUCTION",
    "GENERAL_SYSTEM_INSTRUCTION",
    # Blog Prompts
    "build_blog_article_prompt",
    "build_blog_outline_prompt",
    "build_blog_title_ideas_prompt",
    "build_seo_meta_prompt",
    # Email Prompts
    "build_email_draft_prompt",
    "build_cold_outreach_prompt",
    "build_follow_up_email_prompt",
    "build_email_reply_prompt",
    "build_apology_or_customer_service_prompt",
    # Code Prompts
    "build_code_explanation_prompt",
    "build_code_review_prompt",
    "build_docstring_and_comments_prompt",
    "build_bug_debugging_prompt",
    # Social Prompts
    "build_linkedin_post_prompt",
    "build_twitter_thread_prompt",
    "build_instagram_caption_prompt",
    "build_repurpose_content_prompt",
    # General Prompts
    "build_grammar_check_prompt",
    "build_summarize_prompt",
    "build_paraphrase_prompt",
    "build_tone_adjustment_prompt",
    "build_simplify_text_prompt",
]
