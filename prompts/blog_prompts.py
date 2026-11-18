"""
Blog and long-form article prompt templates for AI WriteMate.
Contains system personas and prompt builders for outlines, articles, titles, and SEO meta.
"""

from typing import Optional, List

BLOG_SYSTEM_INSTRUCTION = """
You are an expert content strategist, journalist, and high-ranking SEO copywriter.
Your goal is to produce engaging, thoroughly researched, logically structured, and original long-form articles.
Key guidelines:
1. Use clear, compelling headings (H2, H3) and scannable formatting.
2. Hook readers in the introduction with an intriguing opening and thesis statement.
3. Deliver high value with concrete examples, actionable takeaways, and engaging transitions.
4. Avoid generic filler, repetitive fluff, and cliché AI phrasing (e.g., 'delve into', 'in today's fast-paced world', 'testament to').
5. Ensure natural keyword integration when keywords are provided.
""".strip()


def build_blog_article_prompt(
    topic: str,
    target_audience: str = "General readers",
    tone: str = "Engaging & Informative",
    target_word_count: int = 800,
    keywords: Optional[List[str]] = None,
    outline: Optional[str] = None,
) -> str:
    """Builds a comprehensive prompt for drafting a full blog post."""
    keywords_str = ", ".join(keywords) if keywords else "None specified"
    outline_section = f"\nUse this structure/outline:\n{outline}\n" if outline else ""

    return f"""
Write a comprehensive, publication-ready blog article on the topic below.

TOPIC: {topic}
TARGET AUDIENCE: {target_audience}
TONE: {tone}
TARGET WORD COUNT: ~{target_word_count} words
SEO KEYWORDS TO INTEGRATE NATURALLY: {keywords_str}
{outline_section}
REQUIREMENTS:
- Catchy, SEO-optimized title at the top.
- Strong introduction with a hook and clear value proposition.
- Structured body sections with markdown H2 and H3 headings.
- Bullet points, bold text, or callout blocks for readability where appropriate.
- Thought-provoking conclusion with a relevant call-to-action (CTA).
- Do not include meta commentary or introductory filler before the title.
""".strip()


def build_blog_outline_prompt(
    topic: str,
    target_audience: str = "General readers",
    tone: str = "Informative",
    num_sections: int = 5,
) -> str:
    """Builds a prompt for generating a structured blog outline."""
    return f"""
Create a comprehensive, well-researched blog outline for the following topic:

TOPIC: {topic}
TARGET AUDIENCE: {target_audience}
TONE: {tone}
DESIRED MAIN SECTIONS: ~{num_sections} sections

FORMAT:
- Working Headline / Title Options (3 variations)
- Hook & Introduction concept
- Main Sections (H2) with 2-3 subpoints (H3) and brief notes on what to cover
- Conclusion & Call-to-Action idea
- Suggested primary & secondary keywords
""".strip()


def build_blog_title_ideas_prompt(
    topic: str,
    num_ideas: int = 8,
    tone: str = "Catchy & Click-worthy",
) -> str:
    """Generates high-CTR blog headlines categorized by style."""
    return f"""
Generate {num_ideas} high-converting blog post titles for the topic: '{topic}'.
TONE: {tone}

Please categorize the ideas into:
1. How-To / Guides
2. Listicle / Numbered
3. Question / Curiosity-Driven
4. Bold / Contrarian
5. SEO-focused / Direct

Ensure each title is under 65 characters so it does not get truncated in search results.
""".strip()


def build_seo_meta_prompt(
    article_summary_or_topic: str,
    keywords: Optional[List[str]] = None,
) -> str:
    """Builds SEO title tag, meta description, and URL slug suggestions."""
    keywords_str = ", ".join(keywords) if keywords else "Relevant to topic"
    return f"""
Generate optimized SEO metadata for the following article context:

CONTEXT / TOPIC:
{article_summary_or_topic}

TARGET KEYWORDS: {keywords_str}

OUTPUT NEEDED:
1. SEO Title Tag (50-60 characters, with primary keyword)
2. Meta Description (145-160 characters, compelling with a CTA)
3. Suggested URL Slug (clean, lowercase, hyphenated)
4. 3-5 Recommended Content Tags / Categories
""".strip()
