"""
Dashboard View - AI WriteMate
Provides writing productivity analytics, document stats, and quick-start studio shortcuts.
"""

import streamlit as st
import pandas as pd
from utils.ui import (
    apply_lavender_theme,
    require_auth,
    render_page_header,
    render_sidebar_user,
)
from modules.history import get_user_history_stats, get_user_documents
from modules.exporter import get_exporter_service

# Page Configuration
st.set_page_config(page_title="Dashboard - AI WriteMate", page_icon="📊", layout="wide")
apply_lavender_theme()
user = require_auth()
render_sidebar_user()

user_id = user["id"]
username = user["username"]

render_page_header(
    title=f"Writer Analytics: {username}",
    subtitle="Track your output, review content volume, and jump directly into creative writing workflows.",
    icon="📊",
)

# Fetch stats and documents
stats = get_user_history_stats(user_id)
documents = get_user_documents(user_id=user_id, limit=100)

# -------------------------------------------------------------
# Top KPI Metric Cards
# -------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{stats.get('total_documents', 0)}</div>
            <div class="stat-label">Total Documents</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{stats.get('total_words', 0):,}</div>
            <div class="stat-label">Total Words Drafted</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    avg_words = int(stats.get('total_words', 0) / max(stats.get('total_documents', 1), 1))
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{avg_words:,}</div>
            <div class="stat-label">Avg Words / Draft</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number" style="font-size: 1.3rem; text-transform: capitalize;">{stats.get('favorite_module', 'None')}</div>
            <div class="stat-label">Primary Module</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# Analytics Breakdown
# -------------------------------------------------------------
col_chart, col_quick = st.columns([3, 2])

with col_chart:
    st.subheader("📈 Output by Category")
    if documents:
        # Group by module_type
        counts = {}
        for d in documents:
            m = d.module_type.capitalize()
            counts[m] = counts.get(m, 0) + 1

        chart_df = pd.DataFrame(list(counts.items()), columns=["Category", "Documents"]).set_index("Category")
        st.bar_chart(chart_df, color="#8b5cf6")
    else:
        st.info("No documents drafted yet. Start creating in the Writing Studio to see charts here!")

with col_quick:
    st.subheader("⚡ Quick Studio Launch")
    st.markdown(
        """
        <div class="lavender-card">
            <h4>Select a Writing Mode:</h4>
            <p>Pick a specialized template to jump right in.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/writing_studio.py", label="📝 Draft Blog Post or Outline", icon="✍️")
    st.page_link("pages/writing_studio.py", label="✉️ Write Executive / Sales Email", icon="📩")
    st.page_link("pages/writing_studio.py", label="💻 Code Review & Walkthrough", icon="💻")
    st.page_link("pages/writing_studio.py", label="📱 Viral Social Media Threads", icon="🚀")
    st.page_link("pages/writing_studio.py", label="🔍 Grammar & Style Polisher", icon="✨")

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# Recent Documents Table & Fast Export
# -------------------------------------------------------------
st.subheader("🗂️ Recent Documents Activity")

if documents:
    exporter = get_exporter_service()
    recent = documents[:5]

    for doc in recent:
        with st.expander(f"📄 {doc.title} — ({doc.module_type.upper()})"):
            c_preview, c_actions = st.columns([3, 1])
            with c_preview:
                st.markdown(f"**Created:** `{doc.created_at[:16] if doc.created_at else 'N/A'}` | **Words:** `{doc.word_count}`")
                st.write(doc.content[:350] + ("..." if len(doc.content) > 350 else ""))

            with c_actions:
                docx_bytes = exporter.export_to_docx(doc.title, doc.content, author=username)
                st.download_button(
                    label="📥 Word (.docx)",
                    data=docx_bytes,
                    file_name=f"{doc.title.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"dash_docx_{doc.id}",
                    use_container_width=True,
                )
                pdf_bytes = exporter.export_to_pdf(doc.title, doc.content, author=username)
                st.download_button(
                    label="📄 PDF (.pdf)",
                    data=pdf_bytes,
                    file_name=f"{doc.title.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    key=f"dash_pdf_{doc.id}",
                    use_container_width=True,
                )
else:
    st.info("No documents found in your library. Use the **Writing Studio** to generate your first document!")
