"""
AI WriteMate - Modern AI-Powered Writing Assistant.
Main entry point handling authentication, lavender theme styling, and session management.
"""

import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Database
from database.db import init_db
from database.auth import authenticate_user, register_user
from utils.ui import (
    apply_lavender_theme,
    init_session_state,
    render_page_header,
    render_sidebar_user,
)
from modules.history import get_user_history_stats, get_user_documents

# Streamlit Page Config
st.set_page_config(
    page_title="AI WriteMate ✍️",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Run DB initialization and theme setup
init_db()
apply_lavender_theme()
init_session_state()


def render_auth_view() -> None:
    """Renders the login and registration portals."""
    render_page_header(
        title="AI WriteMate",
        subtitle="Your intelligent companion for drafting, rewriting, coding, and storytelling.",
        icon="✍️",
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        auth_tab_login, auth_tab_register = st.tabs(["🔑 Log In", "✨ Create Account"])

        # ----------------- LOGIN TAB -----------------
        with auth_tab_login:
            st.markdown("#### Welcome Back")
            st.caption("Sign in to access your writing studio and saved history.")

            with st.form("login_form", clear_on_submit=False):
                login_identifier = st.text_input(
                    "Username or Email",
                    placeholder="e.g. writer_pro or you@example.com",
                )
                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                )
                submit_login = st.form_submit_button("Sign In", use_container_width=True)

                if submit_login:
                    if not login_identifier or not login_password:
                        st.error("Please fill in both fields.")
                    else:
                        with st.spinner("Authenticating..."):
                            success, message, user = authenticate_user(login_identifier, login_password)
                            if success and user:
                                st.session_state["authenticated"] = True
                                st.session_state["user"] = user.to_safe_dict()
                                st.success("Login successful! Redirecting...")
                                st.rerun()
                            else:
                                st.error(message)

        # ----------------- REGISTRATION TAB -----------------
        with auth_tab_register:
            st.markdown("#### New to AI WriteMate?")
            st.caption("Create a free local account in seconds.")

            with st.form("register_form", clear_on_submit=False):
                reg_username = st.text_input("Choose Username", placeholder="e.g. alex_writer")
                reg_email = st.text_input("Email Address", placeholder="e.g. alex@example.com")
                reg_password = st.text_input("Password (min 6 characters)", type="password")
                reg_password_confirm = st.text_input("Confirm Password", type="password")
                submit_register = st.form_submit_button("Create Account", use_container_width=True)

                if submit_register:
                    if not reg_username or not reg_email or not reg_password:
                        st.error("All fields are required.")
                    elif reg_password != reg_password_confirm:
                        st.error("Passwords do not match.")
                    else:
                        with st.spinner("Creating your account..."):
                            success, message, user = register_user(reg_username, reg_email, reg_password)
                            if success and user:
                                st.session_state["authenticated"] = True
                                st.session_state["user"] = user.to_safe_dict()
                                st.success("Account created successfully! Welcome aboard.")
                                st.rerun()
                            else:
                                st.error(message)


def render_authenticated_home() -> None:
    """Renders the authenticated home portal."""
    user = st.session_state.get("user", {})
    username = user.get("username", "Writer")
    user_id = user.get("id")

    render_page_header(
        title=f"Welcome back, {username}!",
        subtitle="What would you like to create today? Select a studio from the sidebar or jump into a quick action below.",
        icon="✨",
    )

    # User Metrics Overview
    stats = get_user_history_stats(user_id) if user_id else {}
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-number">{stats.get('total_documents', 0)}</div>
                <div class="stat-label">Saved Documents</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-number">{stats.get('total_words', 0):,}</div>
                <div class="stat-label">Words Generated</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-number" style="font-size: 1.3rem; text-transform: capitalize;">{stats.get('favorite_module', 'None')}</div>
                <div class="stat-label">Top Category</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-number" style="font-size: 1.1rem; color: #10b981;">Online</div>
                <div class="stat-label">AI Engine Status</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature Portals
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(
            """
            <div class="lavender-card">
                <h3>🚀 Writing Studio</h3>
                <p>Generate high-converting blog posts, marketing emails, social threads, or analyze and debug code snippets with customized personas.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/writing_studio.py", label="Open Writing Studio ➔", icon="🖋️")

    with col_right:
        st.markdown(
            """
            <div class="lavender-card">
                <h3>📚 Document Archive</h3>
                <p>Browse your generation history, search prior drafts, edit saved content, and export directly to Microsoft Word (.docx) or PDF.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/history.py", label="Browse Saved History ➔", icon="📂")

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent Activity Preview
    st.subheader("🕒 Recent Drafts")
    if user_id:
        recent_docs = get_user_documents(user_id=user_id, limit=3)
        if recent_docs:
            for doc in recent_docs:
                with st.expander(f"{doc.title} ({doc.module_type.upper()}) — {doc.created_at[:16] if doc.created_at else ''}"):
                    st.write(doc.content[:300] + ("..." if len(doc.content) > 300 else ""))
                    st.caption(f"Words: {doc.word_count} | Model: {doc.model_used or 'Default'}")
        else:
            st.info("No documents generated yet. Launch the **Writing Studio** to start drafting!")


# -----------------------------------------------------------------
# Main Routing Logic
# -----------------------------------------------------------------
def main():
    # Sidebar
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
            <h2 style="color: #6d28d9; margin: 0;">AI WriteMate</h2>
            <span class="lavender-badge">v1.0 • Streamlit</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("authenticated", False):
        render_sidebar_user()
        render_authenticated_home()
    else:
        render_auth_view()


if __name__ == "__main__":
    main()
