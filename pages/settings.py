"""
Settings & Preferences View - AI WriteMate
Allows users to configure AI providers, API keys, default writing styles, and manage account security.
"""

import os
import streamlit as st
from utils.ui import (
    apply_lavender_theme,
    require_auth,
    render_page_header,
    render_sidebar_user,
)
from database.auth import update_password
from ai.ai_service import (
    get_ai_service,
    PROVIDER_GEMINI,
    PROVIDER_OPENAI,
)

# Streamlit Page Config
st.set_page_config(page_title="Settings - AI WriteMate", page_icon="⚙️", layout="wide")
apply_lavender_theme()
user = require_auth()
render_sidebar_user()

user_id = user["id"]
username = user["username"]
email = user["email"]

render_page_header(
    title="Settings & Preferences",
    subtitle="Manage your AI model keys, default generation preferences, and account security.",
    icon="⚙️",
)

col_main, col_acc = st.columns([3, 2])

# =================================================================
# 1. AI PROVIDER & API KEY CONFIGURATION
# =================================================================
with col_main:
    st.markdown("### 🤖 AI Engine & Model Defaults")
    
    ai_service = get_ai_service()
    configured_providers = ai_service.get_configured_providers()

    st.markdown(
        f"""
        <div class="lavender-card">
            <h4>API Keys Status</h4>
            <p style="margin-bottom: 0.5rem;">
                <b>Google Gemini API:</b> {'🟢 <span style="color: green; font-weight: 600;">Active</span>' if PROVIDER_GEMINI in configured_providers else '🔴 <span style="color: red;">Missing key</span>'}
            </p>
            <p style="margin: 0;">
                <b>OpenAI API:</b> {'🟢 <span style="color: green; font-weight: 600;">Active</span>' if PROVIDER_OPENAI in configured_providers else '🔴 <span style="color: red;">Missing key</span>'}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("🔑 Override API Keys for This Session"):
        st.caption("Keys entered here override your .env file temporarily for this session.")
        new_gemini_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
        new_openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")

        if st.button("Apply API Key Overrides"):
            if new_gemini_key:
                os.environ["GEMINI_API_KEY"] = new_gemini_key
                ai_service.gemini_api_key = new_gemini_key
            if new_openai_key:
                os.environ["OPENAI_API_KEY"] = new_openai_key
                ai_service.openai_api_key = new_openai_key
            st.success("API Keys updated for this session!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎨 Default Generation Parameters")

    def_provider = st.selectbox(
        "Default AI Provider",
        [PROVIDER_GEMINI, PROVIDER_OPENAI],
        format_func=lambda x: "✨ Google Gemini" if x == PROVIDER_GEMINI else "⚡ OpenAI",
        index=0 if st.session_state.get("selected_provider", "gemini") == "gemini" else 1,
    )
    st.session_state["selected_provider"] = def_provider

    models_for_def = ai_service.get_supported_models().get(def_provider, ["gemini-2.5-flash"])
    def_model = st.selectbox("Default Model", options=models_for_def, index=0)
    st.session_state["selected_model"] = def_model

    def_temp = st.slider(
        "Default Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=float(st.session_state.get("temperature", 0.7)),
        step=0.05,
    )
    st.session_state["temperature"] = def_temp

    st.success("Preferences saved in session state.")

# =================================================================
# 2. ACCOUNT SECURITY & PROFILE OVERVIEW
# =================================================================
with col_acc:
    st.markdown("### 👤 Account Overview")
    
    st.markdown(
        f"""
        <div class="lavender-card">
            <p><b>Username:</b> {username}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Account ID:</b> #{user_id}</p>
            <p style="margin: 0;"><b>Member Since:</b> {user.get('created_at', 'Recent')[:10] if user.get('created_at') else 'N/A'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🔒 Change Password")
    with st.form("change_password_form"):
        old_pwd = st.text_input("Current Password", type="password")
        new_pwd = st.text_input("New Password (min 6 chars)", type="password")
        confirm_pwd = st.text_input("Confirm New Password", type="password")
        submit_pwd = st.form_submit_button("Update Password", use_container_width=True)

        if submit_pwd:
            if not old_pwd or not new_pwd:
                st.error("Please fill in all password fields.")
            elif new_pwd != confirm_pwd:
                st.error("New passwords do not match.")
            else:
                success, msg = update_password(user_id, old_pwd, new_pwd)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
