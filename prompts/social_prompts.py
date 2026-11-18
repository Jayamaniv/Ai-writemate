"""
Social media post prompt templates for AI WriteMate.
Covers LinkedIn thought leadership, Twitter/X threads, Instagram captions, and content repurposing.
"""

from typing import Optional, List

SOCIAL_SYSTEM_INSTRUCTION = """
You are a viral social media strategist and digital copywriter specializing in high engagement.
Your goal is to craft platform-native copy that stops the scroll, sparks discussion, and drives shares.
Key guidelines:
1. Master the hook: the first 1-2 lines determine 90% of a post's reach.
2. Platform awareness:
   - LinkedIn: Professional insights, storytelling, line breaks for whitespace, relatable career/business lessons.
   - Twitter/X: Punchy, high-signal-to-noise ratio, numbered thread hooks, under 280 characters per tweet.
   - Instagram: Engaging lifestyle/educational captions, relatable voice, emoji accents, call to comment, hashtag cluster at the end.
   - YouTube: Searchable description, timestamps, hook summary, relevant links placeholder.
3. Include an engaging Call-to-Action (CTA) prompting comments, saves, or clicks.
""".strip()


def build_linkedin_post_prompt(
    topic: str,
    key_insight_or_story: str,
    tone: str = "Inspiring & Professional",
    include_call_to_action: bool = True,
) -> str:
    """Creates a high-performing LinkedIn post."""
    cta_instruction = "Include a question at the end that encourages readers to share their opinions in the comments." if include_call_to_action else ""

    return f"""
Write a high-engagement LinkedIn post based on the following context.

TOPIC: {topic}
KEY LESSON / INSIGHT: {key_insight_or_story}
TONE: {tone}

FORMAT REQUIREMENTS:
- Compelling 1-2 line hook (no generic greetings like 'Happy Monday!').
- Use short paragraphs and white space to optimize for mobile readability.
- Use 1-3 bullet points or emojis to highlight core takeaways without over-cluttering.
- {cta_instruction}
- Add 3-5 relevant, non-spammy hashtags at the bottom.
""".strip()


def build_twitter_thread_prompt(
    topic: str,
    num_tweets: int = 5,
    key_takeaways: Optional[str] = None,
) -> str:
    """Builds a viral Twitter / X thread prompt."""
    takeaways_section = f"KEY TAKEAWAYS TO INCLUDE:\n{key_takeaways}\n" if key_takeaways else ""

    return f"""
Draft an informative and viral {num_tweets}-tweet thread on the following topic.

TOPIC: {topic}
{takeaways_section}

THREAD STRUCTURE:
- Tweet 1 (Hook): Must create intense curiosity or promise high-value payoff. Include a reader incentive (e.g. 'A breakdown in 5 tweets: 🧵').
- Tweets 2 to {num_tweets - 1} (Body): Dense with value, actionable examples, zero fluff. Under 280 characters each.
- Tweet {num_tweets} (Conclusion): Quick summary, a call-to-action (retweet first tweet / follow for more), and open discussion question.

Format each tweet clearly labeled: [Tweet 1/X], [Tweet 2/X], etc.
""".strip()


def build_instagram_caption_prompt(
    topic: str,
    visual_description: Optional[str] = None,
    tone: str = "Casual & Relatable",
    include_hashtags: bool = True,
) -> str:
    """Builds an Instagram caption tailored to imagery or carousels."""
    visual_section = f"VISUAL CONTEXT (Image/Reel/Carousel): {visual_description}\n" if visual_description else ""
    tag_section = "Include a cluster of 10-15 targeted, relevant hashtags separated by line breaks at the bottom." if include_hashtags else "Do not include hashtags."

    return f"""
Write an engaging Instagram caption for the following post.

TOPIC: {topic}
{visual_section}
TONE: {tone}

GUIDELINES:
- Strong visual hook in the first sentence before the '...more' cut-off.
- Tell a micro-story or share a relatable quick tip.
- Natural, aesthetic use of emojis.
- Clear engagement CTA (e.g. 'Save this for later', 'Drop a ❤️ if you agree', 'Tag a friend who needs this').
- {tag_section}
""".strip()


def build_repurpose_content_prompt(
    source_text: str,
    target_platform: str = "LinkedIn",
) -> str:
    """Repurposes existing long-form content (blog, newsletter, speech) into social copy."""
    return f"""
Repurpose the following long-form text into an optimized post for {target_platform}.

ORIGINAL CONTENT:
\"\"\"
{source_text}
\"\"\"

TARGET PLATFORM: {target_platform}

REQUIREMENTS:
- Extract the single most impactful idea or counter-intuitive insight.
- Reformat strictly according to {target_platform}'s native formatting, hook style, and audience expectations.
- Remove all fluff, introductions, or irrelevant tangents from the original text.
- End with a compelling engagement prompt.
""".strip()
