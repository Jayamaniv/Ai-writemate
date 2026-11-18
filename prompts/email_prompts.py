"""
Email drafting and executive communication prompt templates for AI WriteMate.
Covers formal, sales, follow-up, reply, and customer service correspondence.
"""

from typing import Optional

EMAIL_SYSTEM_INSTRUCTION = """
You are an executive communication specialist and master corporate copywriter.
Your goal is to draft clean, polite, persuasive, and context-appropriate emails.
Key guidelines:
1. Always include a concise, high-open-rate Subject Line.
2. Structure emails with a clear greeting, brief context, value proposition/core message, and single unambiguous call-to-action (CTA).
3. Match the specified tone precisely (e.g., formal, friendly, assertive, empathetic).
4. Respect the recipient's time: keep paragraphs short (2-3 sentences max) and use bullet points for lists.
5. Provide placeholder brackets like [Your Name], [Company], or [Date] where custom details belong.
""".strip()


def build_email_draft_prompt(
    recipient: str,
    purpose: str,
    key_points: str,
    tone: str = "Professional",
    sender_name: Optional[str] = None,
    call_to_action: Optional[str] = None,
) -> str:
    """Builds a general-purpose professional email draft prompt."""
    sender_line = f"SENDER: {sender_name}" if sender_name else "SENDER: [Your Name]"
    cta_line = f"DESIRED CALL TO ACTION: {call_to_action}" if call_to_action else "DESIRED CALL TO ACTION: Clear next step"

    return f"""
Draft a complete, ready-to-send email based on the specifications below:

RECIPIENT: {recipient}
PURPOSE: {purpose}
KEY POINTS TO COVER:
{key_points}

TONE: {tone}
{cta_line}
{sender_line}

FORMAT:
- Subject Line: (Give 2 options: direct vs. engaging)
- Email Body: (Greeting, body with paragraphs/bullets, sign-off, signature)
""".strip()


def build_cold_outreach_prompt(
    prospect_role_or_company: str,
    value_proposition: str,
    pain_point: str,
    call_to_action: str = "15-minute introductory call",
) -> str:
    """Generates a high-converting cold outreach email."""
    return f"""
Write a high-converting, concise B2B cold email to a prospective client.

PROSPECT: {prospect_role_or_company}
PAIN POINT ADDRESSED: {pain_point}
VALUE PROPOSITION / SOLUTION: {value_proposition}
CALL TO ACTION: {call_to_action}

GUIDELINES:
- Keep the entire email under 125 words.
- Avoid aggressive or overly salesy jargon.
- Focus on the prospect's benefit, not just our features.
- Provide 2 subject line variants (under 40 characters each).
- Low-friction ask for the call-to-action.
""".strip()


def build_follow_up_email_prompt(
    context: str,
    days_since_last_contact: str = "4 days",
    urgency: str = "Polite & Gentle",
) -> str:
    """Builds a polite follow-up email when no reply has been received."""
    return f"""
Write an effective follow-up email for an unanswered message.

PRIOR CONTEXT / PREVIOUS THREAD:
{context}

TIME ELAPSED: {days_since_last_contact}
URGENCY / TONE: {urgency}

REQUIREMENTS:
- Acknowledge their busy schedule without sounding passive-aggressive.
- Re-state the primary question or action item in 1-2 sentences.
- Make it extremely easy for them to respond (e.g. yes/no or select a time).
- Include a strong, natural subject line referencing the previous thread.
""".strip()


def build_email_reply_prompt(
    incoming_email: str,
    reply_intent: str,
    tone: str = "Professional",
) -> str:
    """Drafts an intelligent reply to an existing email thread."""
    return f"""
Draft a reply to the incoming email below according to the specified intent.

INCOMING EMAIL:
\"\"\"
{incoming_email}
\"\"\"

MY REPLY INTENT & KEY POINTS:
{reply_intent}

TONE: {tone}

FORMAT:
- Direct, context-aware greeting.
- Clear answers to any questions raised in the incoming message.
- Closing and signature placeholder.
""".strip()


def build_apology_or_customer_service_prompt(
    customer_name: str,
    issue_description: str,
    resolution_or_remedy: str,
) -> str:
    """Drafts an empathetic customer service or apology response."""
    return f"""
Draft an empathetic, professional customer service email addressing a user issue.

CUSTOMER: {customer_name}
ISSUE ENCOUNTERED: {issue_description}
RESOLUTION / COMPENSATION OFFERED: {resolution_or_remedy}

GUIDELINES:
- Take sincere ownership without being overly defensive.
- Clearly explain the steps taken to fix the issue and prevent future occurrences.
- State the remedy or compensation clearly.
- Maintain a warm, supportive, and reassuring tone throughout.
""".strip()
