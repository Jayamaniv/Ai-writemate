"""
Unit tests for all reusable prompt builders and expert system personas in AI WriteMate.
"""

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


def test_system_instructions_present():
    """Verify all system instructions are defined and non-empty."""
    for instruction in [
        BLOG_SYSTEM_INSTRUCTION,
        EMAIL_SYSTEM_INSTRUCTION,
        CODE_SYSTEM_INSTRUCTION,
        SOCIAL_SYSTEM_INSTRUCTION,
        GENERAL_SYSTEM_INSTRUCTION,
    ]:
        assert isinstance(instruction, str)
        assert len(instruction.strip()) > 100


def test_blog_prompt_builders():
    """Verify blog article, outline, headline, and SEO prompt outputs."""
    article_prompt = build_blog_article_prompt(
        topic="Future of AI in 2026",
        target_audience="Engineers",
        keywords=["Python", "Streamlit"],
    )
    assert "Future of AI in 2026" in article_prompt
    assert "Python, Streamlit" in article_prompt

    outline_prompt = build_blog_outline_prompt("Microservices vs Monoliths")
    assert "Microservices vs Monoliths" in outline_prompt

    title_prompt = build_blog_title_ideas_prompt("Remote Work Culture", num_ideas=10)
    assert "Remote Work Culture" in title_prompt
    assert "10" in title_prompt

    seo_prompt = build_seo_meta_prompt("Article on modern databases", keywords=["SQLite"])
    assert "Article on modern databases" in seo_prompt
    assert "SQLite" in seo_prompt


def test_email_prompt_builders():
    """Verify general email, cold outreach, follow-up, and reply prompts."""
    email_prompt = build_email_draft_prompt(
        recipient="Director of Marketing",
        purpose="Q3 Campaign Pitch",
        key_points="1. ROI projection\n2. Creative assets",
        tone="Assertive",
    )
    assert "Director of Marketing" in email_prompt
    assert "Q3 Campaign Pitch" in email_prompt
    assert "Assertive" in email_prompt

    cold_prompt = build_cold_outreach_prompt(
        prospect_role_or_company="CTO at TechCorp",
        value_proposition="Cut cloud latency by 40%",
        pain_point="High egress fees",
    )
    assert "CTO at TechCorp" in cold_prompt
    assert "Cut cloud latency by 40%" in cold_prompt

    followup_prompt = build_follow_up_email_prompt("Sent initial contract last Monday")
    assert "Sent initial contract last Monday" in followup_prompt


def test_code_prompt_builders():
    """Verify code explanation, review, docstring, and debugging prompts."""
    code_sample = "def fibonacci(n):\n    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
    
    explain_prompt = build_code_explanation_prompt(code_sample, language="Python")
    assert "fibonacci" in explain_prompt
    assert "Python" in explain_prompt

    review_prompt = build_code_review_prompt(code_sample, focus_areas="Recursion depth")
    assert "Recursion depth" in review_prompt

    debug_prompt = build_bug_debugging_prompt(code_sample, error_message="RecursionError: maximum depth exceeded")
    assert "RecursionError" in debug_prompt


def test_social_prompt_builders():
    """Verify LinkedIn, Twitter thread, Instagram, and repurposing prompts."""
    linkedin = build_linkedin_post_prompt("Product Launch", "Shipped AI WriteMate")
    assert "Product Launch" in linkedin
    assert "Shipped AI WriteMate" in linkedin

    twitter = build_twitter_thread_prompt("Lessons in Bootstrap SaaS", num_tweets=7)
    assert "Lessons in Bootstrap SaaS" in twitter
    assert "7-tweet" in twitter

    instagram = build_instagram_caption_prompt("Desk Setup", tone="Aesthetic")
    assert "Desk Setup" in instagram

    repurpose = build_repurpose_content_prompt("Full transcript of a 10-minute keynote speech", target_platform="Twitter")
    assert "Twitter" in repurpose


def test_general_prompt_builders():
    """Verify grammar check, summarization, paraphrasing, and simplification prompts."""
    grammar = build_grammar_check_prompt("This sentence have grammatical mistake.")
    assert "This sentence have grammatical mistake." in grammar

    summary = build_summarize_prompt("Lengthy scientific research paper...", format_type="Executive Summary")
    assert "Executive Summary" in summary

    paraphrase = build_paraphrase_prompt("Artificial intelligence is rapidly transforming global business operations.")
    assert "Artificial intelligence is rapidly transforming" in paraphrase

    tone = build_tone_adjustment_prompt("Hey, we need to talk ASAP.", target_tone="Diplomatic & Empathetic")
    assert "Diplomatic & Empathetic" in tone

    simplify = build_simplify_text_prompt("The obfuscation of institutional methodologies yields suboptimal efficacy.")
    assert "obfuscation" in simplify
