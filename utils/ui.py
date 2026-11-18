"""
UI helper functions and lavender styling injection for AI WriteMate.
Contains theme CSS, session state management, and authentication guards.
"""

import streamlit as st
from typing import Optional, Dict, Any

# Lavender Color Palette
LAVENDER_DARK = "#6d28d9"
LAVENDER_PRIMARY = "#8b5cf6"
LAVENDER_LIGHT = "#a78bfa"
LAVENDER_SURFACE = "#f5f3ff"
LAVENDER_BORDER = "#ddd6fe"
TEXT_DARK = "#1e1b4b"


def apply_lavender_theme() -> None:
    """Injects high-polish lavender CSS styles into the Streamlit app."""
    css = f"""
    <style>
    /* Main Background & Typography */
    .stApp {{
        background: linear-gradient(180deg, #fbfbfe 0%, #f5f3ff 100%);
        color: {TEXT_DARK};
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: #f8f6fe !important;
        border-right: 1px solid {LAVENDER_BORDER};
    }}

    /* Custom Header Banner */
    .lavender-hero {{
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 50%, #c084fc 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(139, 92, 246, 0.25);
    }}

    .lavender-hero h1 {{
        color: white !important;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.025em;
    }}

    .lavender-hero p {{
        color: #f3e8ff !important;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }}

    /* Lavender Card Container */
    .lavender-card {{
        background: #ffffff;
        border: 1px solid {LAVENDER_BORDER};
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .lavender-card:hover {{
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.12);
    }}

    /* Metric Stat Box */
    .stat-box {{
        background: #ffffff;
        border: 1px solid {LAVENDER_BORDER};
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(139, 92, 246, 0.06);
    }}

    .stat-number {{
        font-size: 2rem;
        font-weight: 700;
        color: {LAVENDER_DARK};
        margin: 0;
    }}

    .stat-label {{
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }}

    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.4rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2) !important;
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
        box-shadow: 0 6px 18px rgba(124, 58, 237, 0.35) !important;
        transform: translateY(-1px);
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: #f1edfe;
        padding: 6px;
        border-radius: 12px;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 8px 18px;
        color: {TEXT_DARK};
        font-weight: 600;
        border: none !important;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: white !important;
        color: {LAVENDER_DARK} !important;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.15) !important;
    }}

    /* Badges */
    .lavender-badge {{
        display: inline-block;
        background: #ede9fe;
        color: {LAVENDER_DARK};
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def init_session_state() -> None:
    """Initializes standard session state keys if not already set."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "selected_provider" not in st.session_state:
        st.session_state["selected_provider"] = "gemini"
    if "selected_model" not in st.session_state:
        st.session_state["selected_model"] = "gemini-2.5-flash"
    if "temperature" not in st.session_state:
        st.session_state["temperature"] = 0.7


def require_auth() -> Dict[str, Any]:
    """
    Guards a page requiring authentication.
    If unauthenticated, halts execution and presents an informative banner.
    Returns the authenticated user dict.
    """
    init_session_state()
    if not st.session_state.get("authenticated", False):
        st.warning("🔒 Please sign in from the main app page to access this studio.")
        st.info("Navigate back to the home page (`app.py`) to log in or create an account.")
        st.stop()
    return st.session_state["user"]


def render_page_header(title: str, subtitle: str, icon: str = "✍️") -> None:
    """Renders the standard lavender hero banner."""
    html_banner = f"""
    <div class="lavender-hero">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """
    st.markdown(html_banner, unsafe_allow_html=True)


def render_sidebar_user() -> None:
    """Renders user info and a logout button in the sidebar."""
    if st.session_state.get("authenticated", False):
        user = st.session_state.get("user", {})
        username = user.get("username", "Writer")
        email = user.get("email", "")

        st.sidebar.markdown(f"### 👤 Logged in as **{username}**")
        st.sidebar.caption(email)
        
        if st.sidebar.button("🚪 Log Out", key="sidebar_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            st.rerun()
        st.sidebar.markdown("---")
