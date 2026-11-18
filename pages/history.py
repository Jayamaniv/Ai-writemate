"""
History and Document Library View - AI WriteMate
Allows users to browse, search, edit, delete, and re-export saved generation history.
"""

import streamlit as st
from utils.ui import (
    apply_lavender_theme,
    require_auth,
    render_page_header,
    render_sidebar_user,
)
from modules.history import (
    get_user_documents,
    get_document_by_id,
    update_document,
    delete_document,
)
from modules.exporter import get_exporter_service

# Streamlit Page Config
st.set_page_config(page_title="Document Library - AI WriteMate", page_icon="📚", layout="wide")
apply_lavender_theme()
user = require_auth()
render_sidebar_user()

user_id = user["id"]
username = user["username"]

render_page_header(
    title="Document Library & Archive",
    subtitle="Search through all your previous AI drafts, edit content directly, and export to DOCX or PDF.",
    icon="📚",
)

exporter = get_exporter_service()

# -------------------------------------------------------------
# Search & Filter Toolbar
# -------------------------------------------------------------
c_search, c_filter, c_refresh = st.columns([3, 2, 1])

with c_search:
    search_query = st.text_input("🔍 Search by title or content keywords...", placeholder="e.g. artificial intelligence, marketing email, Python")

with c_filter:
    category_filter = st.selectbox(
        "Filter by Module",
        ["All", "blog", "email", "code", "social", "grammar", "summary", "rewrite", "polish"],
        format_func=lambda x: f"Category: {x.capitalize()}",
    )

with c_refresh:
    st.write("")
    st.write("")
    if st.button("🔄 Refresh Library", use_container_width=True):
        st.rerun()

# Fetch documents
docs = get_user_documents(
    user_id=user_id,
    limit=100,
    module_type=category_filter if category_filter != "All" else None,
    search_query=search_query if search_query.strip() else None,
)

if not docs:
    st.info("No documents found matching your filter criteria. Create something new in the **Writing Studio**!")
else:
    st.markdown(f"**Found {len(docs)} document(s):**")
    
    col_list, col_editor = st.columns([2, 3])

    with col_list:
        st.markdown("#### Saved Drafts")
        selected_doc_id = st.radio(
            "Select a document to inspect or edit:",
            options=[d.id for d in docs],
            format_func=lambda doc_id: next(
                f"{d.title} ({d.module_type.upper()}) • {d.created_at[:10] if d.created_at else ''}"
                for d in docs if d.id == doc_id
            ),
            label_visibility="collapsed",
        )

    # -------------------------------------------------------------
    # Document Inspection & Live Editing Pane
    # -------------------------------------------------------------
    with col_editor:
        selected_doc = next((d for d in docs if d.id == selected_doc_id), None)

        if selected_doc:
            st.markdown(
                f"""
                <div class="lavender-card">
                    <span class="lavender-badge">{selected_doc.module_type.upper()}</span>
                    <h3 style="margin-top: 0.5rem; margin-bottom: 0.25rem;">{selected_doc.title}</h3>
                    <p style="color: #64748b; font-size: 0.85rem; margin: 0;">
                        Words: <b>{selected_doc.word_count}</b> | 
                        Model: <b>{selected_doc.model_used or 'Default'}</b> | 
                        Created: <b>{selected_doc.created_at[:16] if selected_doc.created_at else ''}</b>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.form(f"edit_doc_form_{selected_doc.id}"):
                edit_title = st.text_input("Document Title", value=selected_doc.title)
                edit_content = st.text_area("Document Content (Markdown)", value=selected_doc.content, height=350)
                
                c_save, c_del = st.columns([3, 1])
                with c_save:
                    save_btn = st.form_submit_button("💾 Save Edits", use_container_width=True)
                with c_del:
                    del_btn = st.form_submit_button("🗑️ Delete Draft", use_container_width=True)

                if save_btn:
                    if update_document(selected_doc.id, user_id, edit_title, edit_content):
                        st.success("Document updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update document.")

                if del_btn:
                    if delete_document(selected_doc.id, user_id):
                        st.success("Document deleted.")
                        st.rerun()
                    else:
                        st.error("Could not delete document.")

            # Direct Exports
            st.markdown("##### 📥 Export Options")
            c1, c2, c3 = st.columns(3)

            with c1:
                docx_bytes = exporter.export_to_docx(selected_doc.title, selected_doc.content, author=username)
                st.download_button(
                    label="📄 Word (.docx)",
                    data=docx_bytes,
                    file_name=f"{selected_doc.title.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"hist_docx_{selected_doc.id}",
                    use_container_width=True,
                )

            with c2:
                pdf_bytes = exporter.export_to_pdf(selected_doc.title, selected_doc.content, author=username)
                st.download_button(
                    label="📑 PDF (.pdf)",
                    data=pdf_bytes,
                    file_name=f"{selected_doc.title.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    key=f"hist_pdf_{selected_doc.id}",
                    use_container_width=True,
                )

            with c3:
                md_text = exporter.export_to_markdown(selected_doc.title, selected_doc.content)
                st.download_button(
                    label="📝 Markdown (.md)",
                    data=md_text,
                    file_name=f"{selected_doc.title.replace(' ', '_')}.md",
                    mime="text/markdown",
                    key=f"hist_md_{selected_doc.id}",
                    use_container_width=True,
                )
