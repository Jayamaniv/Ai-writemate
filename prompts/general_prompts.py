"""
General writing, proofreading, grammar, summarization, and rewriting templates for AI WriteMate.
Contains prompt builders for tone adjustment, text simplification, paraphrasing, and executive summaries.
"""

from typing import Optional

GENERAL_SYSTEM_INSTRUCTION = """
You are a master editor, linguist, and communication specialist.
Your goal is to polish, clarify, transform, and distill written content while preserving the original intent and core meaning.
Key guidelines:
1. Prioritize clarity, precision, and natural sentence rhythm.
2. Eliminate redundant words, passive-voice clutter, and grammatical awkwardness.
3. Faithfully adopt requested tones (e.g. Executive, Casual, Academic, Persuasive, Empathetic).
4. For proofreading, clearly delineate between the corrected output and the explanation of changes.
5. In summarization, maintain factual integrity with zero hallucinations.
""".strip()


def build_grammar_check_prompt(
    text: str,
    style_guide: str = "Standard Professional English",
    show_explanations: bool = True,
) -> str:
    """Builds a prompt for grammar correction, spellcheck, and syntax improvement."""
    explain_req = """
2. List of Improvements: Bullet points showing:
   - Original phrase -> Corrected phrase
   - Rule / Reason for change (e.g., subject-verb agreement, comma splice, clarity)
""" if show_explanations else ""

    return f"""
Proofread and correct the following text for grammar, punctuation, spelling, syntax, and flow.

STYLE GUIDE / STANDARD: {style_guide}

INPUT TEXT:
\"\"\"
{text}
\"\"\"

PLEASE PROVIDE:
1. Fully Polished Version: The clean, corrected text ready to use.
{explain_req}
""".strip()


def build_summarize_prompt(
    text: str,
    format_type: str = "Bullet Points",
    target_length: str = "Medium (~150-250 words)",
) -> str:
    """Builds a summarization prompt supporting executive summaries, TL;DR, or key takeaways."""
    return f"""
Summarize the following content accurately and concisely.

INPUT TEXT:
\"\"\"
{text}
\"\"\"

SUMMARY FORMAT: {format_type} (e.g., TL;DR + Key Bullet Points, Executive Paragraph, or One-Sentence Takeaway)
DESIRED LENGTH: {target_length}

REQUIREMENTS:
- Capture all central arguments and conclusions without distortion.
- Omit anecdotal details, filler, and repetitive points.
- If bullet points are requested, ensure each bullet begins with a bold keyword or phrase.
""".strip()


def build_paraphrase_prompt(
    text: str,
    goal: str = "Enhance clarity, vocabulary, and flow",
    tone: str = "Natural",
    num_variants: int = 3,
) -> str:
    """Generates multiple paraphrased variations of an input text."""
    return f"""
Paraphrase the following text into {num_variants} distinct variations.

ORIGINAL TEXT:
\"\"\"
{text}
\"\"\"

PARAPHRASING GOAL: {goal}
TARGET TONE: {tone}

REQUIREMENTS:
- Provide {num_variants} distinct rewrites:
  1. Variation 1: Direct & Concise (streamlined for speed and brevity)
  2. Variation 2: Engaging & Expressive (rich vocabulary and varied rhythm)
  3. Variation 3: Formal / Executive (authoritative and polished)
- Ensure none of the core facts or meaning are altered.
""".strip()


def build_tone_adjustment_prompt(
    text: str,
    target_tone: str = "Professional",
    context: Optional[str] = None,
) -> str:
    """Rewrites text to match a specific emotional or stylistic tone."""
    context_section = f"AUDIENCE / CONTEXT: {context}\n" if context else ""

    return f"""
Rewrite the following passage to strictly match the requested tone.

TARGET TONE: {target_tone} (e.g., Professional, Empathetic, Humorous, Academic, Urgent, Conversational)
{context_section}
ORIGINAL TEXT:
\"\"\"
{text}
\"\"\"

REQUIREMENTS:
- Rewrite the text so its vocabulary, sentence structure, and emotional resonance match '{target_tone}'.
- Preserve all underlying information and intended message.
- Provide the transformed passage directly.
""".strip()


def build_simplify_text_prompt(
    text: str,
    target_reading_level: str = "Plain English (8th-grade level)",
) -> str:
    """Simplifies complex or jargon-heavy text for general readability."""
    return f"""
Simplify the following text so that it can be effortlessly understood by anyone.

TARGET READING LEVEL: {target_reading_level}

ORIGINAL TEXT:
\"\"\"
{text}
\"\"\"

GUIDELINES:
- Replace industry jargon, bureaucratic phrases, and obscure vocabulary with simple, everyday equivalents.
- Break up long, convoluted run-on sentences into short, direct statements.
- Use active voice instead of passive voice.
- Maintain 100% of the original meaning and core insight.
""".strip()
