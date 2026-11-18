"""
Writing Studio - AI WriteMate
Comprehensive interactive studio for blog articles, emails, code analysis, social media, and grammar polishing.
Includes real-time streaming, interactive model controls, and instant PDF/Word exports.
"""

import streamlit as st
from utils.ui import (
    apply_lavender_theme,
    require_auth,
    render_page_header,
    render_sidebar_user,
)
from ai.ai_service import (
    get_ai_service,
    PROVIDER_GEMINI,
    PROVIDER_OPENAI,
)
from modules.writing import get_writing_module
from modules.grammar import get_grammar_module
from modules.summarizer import get_summarizer_module
from modules.rewriter import get_rewriter_module
from modules.exporter import get_exporter_service
from modules.history import save_document

# Streamlit Page Config
st.set_page_config(page_title="Writing Studio - AI WriteMate", page_icon="🖋️", layout="wide")
apply_lavender_theme()
user = require_auth()
render_sidebar_user()

user_id = user["id"]
username = user["username"]

render_page_header(
    title="AI Writing Studio",
    subtitle="Choose your craft below: draft full blogs, executive correspondence, social campaigns, or polish existing text.",
    icon="🖋️",
)

# -----------------------------------------------------------------
# Sidebar Interactive AI Controls
# -----------------------------------------------------------------
st.sidebar.markdown("### ⚙️ AI Engine Settings")

ai_service = get_ai_service()
supported_models = ai_service.get_supported_models()

provider_choice = st.sidebar.selectbox(
    "AI Provider",
    options=[PROVIDER_GEMINI, PROVIDER_OPENAI],
    format_func=lambda x: "✨ Google Gemini" if x == PROVIDER_GEMINI else "⚡ OpenAI",
    index=0 if st.session_state.get("selected_provider", "gemini") == "gemini" else 1,
)

available_models = supported_models.get(provider_choice, ["gemini-2.5-flash"])
model_choice = st.sidebar.selectbox(
    "Model Selection",
    options=available_models,
    index=0,
)

temperature = st.sidebar.slider(
    "Creativity (Temperature)",
    min_value=0.0,
    max_value=1.0,
    value=float(st.session_state.get("temperature", 0.7)),
    step=0.05,
    help="Lower values are more deterministic and precise; higher values are more creative.",
)

enable_streaming = st.sidebar.toggle("⚡ Stream Generation", value=True)
auto_save_history = st.sidebar.toggle("💾 Save to Library Automatically", value=True)

# Instantiate Module Services
writing_mod = get_writing_module()
grammar_mod = get_grammar_module()
summarizer_mod = get_summarizer_module()
rewriter_mod = get_rewriter_module()
exporter = get_exporter_service()


def render_export_bar(doc_title: str, doc_content: str, key_prefix: str):
    """Renders download buttons for Word (.docx), PDF (.pdf), and Markdown."""
    st.markdown("---")
    st.markdown("##### 📥 Export Document")
    c1, c2, c3 = st.columns(3)

    with c1:
        docx_bytes = exporter.export_to_docx(doc_title, doc_content, author=username)
        st.download_button(
            label="📄 Download Word (.docx)",
            data=docx_bytes,
            file_name=f"{doc_title.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key=f"{key_prefix}_docx",
            use_container_width=True,
        )

    with c2:
        pdf_bytes = exporter.export_to_pdf(doc_title, doc_content, author=username)
        st.download_button(
            label="📑 Download PDF (.pdf)",
            data=pdf_bytes,
            file_name=f"{doc_title.replace(' ', '_')}.pdf",
            mime="application/pdf",
            key=f"{key_prefix}_pdf",
            use_container_width=True,
        )

    with c3:
        md_text = exporter.export_to_markdown(doc_title, doc_content)
        st.download_button(
            label="📝 Download Markdown (.md)",
            data=md_text,
            file_name=f"{doc_title.replace(' ', '_')}.md",
            mime="text/markdown",
            key=f"{key_prefix}_md",
            use_container_width=True,
        )


# -----------------------------------------------------------------
# Main Studio Tabs
# -----------------------------------------------------------------
tab_blog, tab_email, tab_code, tab_social, tab_polish = st.tabs([
    "📝 Blog & Articles",
    "✉️ Email Assistant",
    "💻 Code Studio",
    "📱 Social Media",
    "✨ Polish & Rewrite",
])

# =================================================================
# 1. BLOG & LONG-FORM ARTICLES
# =================================================================
with tab_blog:
    st.markdown("#### 📰 Blog & Long-Form Content Creator")
    
    blog_mode = st.radio(
        "Workflow",
        ["Full Article", "Structured Outline", "Title Generator", "SEO Metadata"],
        horizontal=True,
    )

    col_in, col_opts = st.columns([3, 2])
    with col_in:
        blog_topic = st.text_input("Article Topic / Headline", placeholder="e.g. How Autonomous AI Agents Are Transforming Software in 2026")
        blog_outline_custom = st.text_area("Optional Outline / Key Subtopics", placeholder="Optional bullet points or sections to include...", height=100)

    with col_opts:
        blog_tone = st.selectbox("Tone of Voice", ["Engaging & Informative", "Authoritative & Research-Backed", "Casual & Conversational", "Inspirational & Storytelling", "Contrarian & Thought-Provoking"])
        blog_audience = st.text_input("Target Audience", value="Professionals & Tech Enthusiasts")
        blog_words = st.slider("Target Word Count", min_value=300, max_value=2500, value=800, step=100)
        blog_keywords = st.text_input("SEO Keywords (comma separated)", placeholder="e.g. AI Agents, LLM, Streamlit")

    if st.button("🚀 Generate Content", key="btn_gen_blog", use_container_width=True):
        if not blog_topic.strip():
            st.error("Please enter a topic before generating.")
        else:
            kw_list = [k.strip() for k in blog_keywords.split(",") if k.strip()] if blog_keywords else None
            
            with st.spinner("Drafting content with AI..."):
                try:
                    if enable_streaming:
                        out_area = st.empty()
                        stream_gen = writing_mod.stream_blog_post(
                            topic=blog_topic,
                            target_audience=blog_audience,
                            tone=blog_tone,
                            target_word_count=blog_words,
                            keywords=kw_list,
                            outline=blog_outline_custom,
                            provider=provider_choice,
                            model=model_choice,
                            temperature=temperature,
                        )
                        full_content = ""
                        for chunk in stream_gen:
                            full_content += chunk
                            out_area.markdown(full_content)
                    else:
                        response = writing_mod.write_blog_post(
                            topic=blog_topic,
                            target_audience=blog_audience,
                            tone=blog_tone,
                            target_word_count=blog_words,
                            keywords=kw_list,
                            outline=blog_outline_custom,
                            provider=provider_choice,
                            model=model_choice,
                            temperature=temperature,
                        )
                        full_content = response.text
                        st.markdown(full_content)

                    # Auto-save
                    if auto_save_history and full_content:
                        save_document(
                            user_id=user_id,
                            title=f"Blog: {blog_topic[:50]}",
                            content=full_content,
                            module_type="blog",
                            model_used=model_choice,
                        )
                        st.success("✅ Saved to your personal library!")

                    render_export_bar(doc_title=blog_topic, doc_content=full_content, key_prefix="blog")

                except Exception as exc:
                    st.error(f"Generation error: {str(exc)}")

# =================================================================
# 2. EMAIL ASSISTANT
# =================================================================
with tab_email:
    st.markdown("#### ✉️ Executive & Marketing Email Assistant")

    c_em_in, c_em_opts = st.columns([3, 2])
    with c_em_in:
        email_recipient = st.text_input("Recipient (Name / Role)", placeholder="e.g. VP of Product, Hiring Manager, Client")
        email_purpose = st.text_input("Email Purpose / Context", placeholder="e.g. Schedule a demo call after product launch")
        email_key_points = st.text_area("Key Points to Cover", placeholder="1. Mention mutual connection\n2. Highlight 30% speed increase\n3. Request 15 min call next Tuesday", height=120)

    with c_em_opts:
        email_tone = st.selectbox("Email Tone", ["Professional", "Assertive & Direct", "Warm & Friendly", "Urgent", "Empathetic"])
        email_cta = st.text_input("Call to Action (CTA)", value="15-minute introductory call")
        email_sender = st.text_input("Sender Sign-off Name", value=username)

    if st.button("✉️ Draft Email", key="btn_gen_email", use_container_width=True):
        if not email_purpose.strip() or not email_key_points.strip():
            st.error("Please fill in the email purpose and key points.")
        else:
            with st.spinner("Drafting email..."):
                try:
                    if enable_streaming:
                        out_area = st.empty()
                        stream_gen = writing_mod.stream_email(
                            recipient=email_recipient,
                            purpose=email_purpose,
                            key_points=email_key_points,
                            tone=email_tone,
                            sender_name=email_sender,
                            call_to_action=email_cta,
                            provider=provider_choice,
                            model=model_choice,
                        )
                        full_content = ""
                        for chunk in stream_gen:
                            full_content += chunk
                            out_area.markdown(full_content)
                    else:
                        resp = writing_mod.write_email(
                            recipient=email_recipient,
                            purpose=email_purpose,
                            key_points=email_key_points,
                            tone=email_tone,
                            sender_name=email_sender,
                            call_to_action=email_cta,
                            provider=provider_choice,
                            model=model_choice,
                        )
                        full_content = resp.text
                        st.markdown(full_content)

                    if auto_save_history and full_content:
                        save_document(
                            user_id=user_id,
                            title=f"Email: {email_purpose[:40]}",
                            content=full_content,
                            module_type="email",
                            model_used=model_choice,
                        )
                        st.success("✅ Saved to your personal library!")

                    render_export_bar(doc_title=f"Email - {email_purpose}", doc_content=full_content, key_prefix="email")

                except Exception as exc:
                    st.error(f"Generation error: {str(exc)}")

# =================================================================
# 3. CODE STUDIO
# =================================================================
with tab_code:
    st.markdown("#### 💻 Technical Documentation & Code Review")

    code_mode = st.radio("Task", ["Explain Code Architecture", "Perform Code Review", "Add Docstrings & Comments", "Debug Bug"], horizontal=True)
    c_code_in, c_code_opt = st.columns([3, 1])

    with c_code_in:
        code_input = st.text_area("Paste Code Snippet", placeholder="def process_data(items):\n    # paste your code here...", height=200)

    with c_code_opt:
        code_lang = st.selectbox("Language", ["Python", "JavaScript/TypeScript", "SQL", "HTML/CSS", "Go", "Java", "C++", "Rust"])
        code_audience = st.selectbox("Target Depth", ["Junior Developer", "Senior Engineer", "Non-Technical Stakeholder"])

    if st.button("💻 Analyze Code", key="btn_gen_code", use_container_width=True):
        if not code_input.strip():
            st.error("Please paste code to analyze.")
        else:
            with st.spinner("Analyzing code..."):
                try:
                    if "Explain" in code_mode:
                        resp = writing_mod.explain_code(
                            code_snippet=code_input,
                            language=code_lang,
                            target_audience=code_audience,
                            provider=provider_choice,
                            model=model_choice,
                        )
                    elif "Review" in code_mode:
                        resp = writing_mod.review_code(
                            code_snippet=code_input,
                            language=code_lang,
                            provider=provider_choice,
                            model=model_choice,
                        )
                    else:
                        resp = writing_mod.explain_code(
                            code_snippet=code_input,
                            language=code_lang,
                            provider=provider_choice,
                            model=model_choice,
                        )

                    st.markdown(resp.text)
                    if auto_save_history and resp.text:
                        save_document(
                            user_id=user_id,
                            title=f"Code: {code_mode} ({code_lang})",
                            content=resp.text,
                            module_type="code",
                            model_used=model_choice,
                        )
                        st.success("✅ Saved to your personal library!")

                    render_export_bar(doc_title=f"Code Analysis - {code_lang}", doc_content=resp.text, key_prefix="code")

                except Exception as exc:
                    st.error(f"Analysis error: {str(exc)}")

# =================================================================
# 4. SOCIAL MEDIA
# =================================================================
with tab_social:
    st.markdown("#### 📱 Viral Social Media Studio")

    soc_platform = st.selectbox("Platform", ["LinkedIn Post", "Twitter / X Thread (5 Tweets)", "Instagram Caption", "Repurpose Existing Text"])
    soc_topic = st.text_input("Campaign Focus / Topic", placeholder="e.g. 5 lessons from building an AI SaaS in 30 days")
    soc_details = st.text_area("Key Takeaways or Draft Text to Repurpose", placeholder="Add raw thoughts, bullets, or paste an article...", height=120)

    if st.button("🚀 Generate Social Copy", key="btn_gen_soc", use_container_width=True):
        if not soc_topic.strip() and not soc_details.strip():
            st.error("Please provide a topic or details.")
        else:
            with st.spinner("Crafting social copy..."):
                try:
                    resp = writing_mod.write_social_post(
                        platform=soc_platform,
                        topic=soc_topic or "Social Campaign",
                        details=soc_details,
                        provider=provider_choice,
                        model=model_choice,
                    )
                    st.markdown(resp.text)

                    if auto_save_history and resp.text:
                        save_document(
                            user_id=user_id,
                            title=f"Social ({soc_platform}): {soc_topic[:35]}",
                            content=resp.text,
                            module_type="social",
                            model_used=model_choice,
                        )
                        st.success("✅ Saved to your personal library!")

                    render_export_bar(doc_title=f"Social Post - {soc_platform}", doc_content=resp.text, key_prefix="social")

                except Exception as exc:
                    st.error(f"Generation error: {str(exc)}")

# =================================================================
# 5. POLISH & REWRITE
# =================================================================
with tab_polish:
    st.markdown("#### ✨ Polish, Proofread & Paraphrase")

    polish_mode = st.radio("Tool", ["Grammar & Style Check", "Smart Summarizer", "Paraphrase (3 Variations)", "Tone Shift", "Simplify (Plain English)"], horizontal=True)
    polish_input = st.text_area("Original Text", placeholder="Paste the text you want to improve, rewrite, or summarize...", height=160)

    c_p1, c_p2 = st.columns(2)
    with c_p1:
        target_tone = st.selectbox("Desired Tone / Target", ["Professional & Executive", "Casual & Engaging", "Academic & Rigorous", "Persuasive & Sales-Oriented", "Empathetic & Caring"])
    with c_p2:
        sum_format = st.selectbox("Summary Format (if summarizing)", ["Bullet Points", "Executive Paragraph", "One-Sentence TL;DR"])

    if st.button("✨ Refine Text", key="btn_gen_polish", use_container_width=True):
        if not polish_input.strip():
            st.error("Please enter text to refine.")
        else:
            with st.spinner("Polishing content..."):
                try:
                    if "Grammar" in polish_mode:
                        resp = grammar_mod.check_grammar(
                            text=polish_input,
                            provider=provider_choice,
                            model=model_choice,
                        )
                    elif "Summarizer" in polish_mode:
                        if "TL;DR" in sum_format:
                            resp = summarizer_mod.generate_tldr(
                                text=polish_input,
                                provider=provider_choice,
                                model=model_choice,
                            )
                        else:
                            resp = summarizer_mod.summarize(
                                text=polish_input,
                                format_type=sum_format,
                                provider=provider_choice,
                                model=model_choice,
                            )
                    elif "Paraphrase" in polish_mode:
                        resp = rewriter_mod.paraphrase(
                            text=polish_input,
                            provider=provider_choice,
                            model=model_choice,
                        )
                    elif "Tone" in polish_mode:
                        resp = rewriter_mod.adjust_tone(
                            text=polish_input,
                            target_tone=target_tone,
                            provider=provider_choice,
                            model=model_choice,
                        )
                    else:
                        resp = rewriter_mod.simplify(
                            text=polish_input,
                            provider=provider_choice,
                            model=model_choice,
                        )

                    st.markdown(resp.text)
                    if auto_save_history and resp.text:
                        save_document(
                            user_id=user_id,
                            title=f"Polished: {polish_mode}",
                            content=resp.text,
                            module_type="polish",
                            model_used=model_choice,
                        )
                        st.success("✅ Saved to your personal library!")

                    render_export_bar(doc_title=f"Polished Text ({polish_mode})", doc_content=resp.text, key_prefix="polish")

                except Exception as exc:
                    st.error(f"Processing error: {str(exc)}")
