# AI WriteMate ✍️🤖

**AI WriteMate** is an intelligent, full-featured AI writing studio built with Python and Streamlit. It enables users to draft, rewrite, summarize, explain code, and polish content across multiple formats (blogs, executive emails, social campaigns, code reviews) with dual-provider LLM support (**Google Gemini** and **OpenAI**), real-time streaming, and 1-click **Word (.docx)** and **PDF** exports.

---

## ✨ Key Features

- **🎨 Modern Lavender UI:** Custom styled Streamlit interface featuring a high-contrast lavender theme, responsive sidebar navigation, and card-based layouts.
- **🔐 Secure Authentication:** User registration and sign-in powered by **SQLite** and **bcrypt** password hashing (12 salt rounds) with session state guards.
- **⚡ Dual AI Engine with Dynamic Switching:** Seamlessly toggle between **Google Gemini** (`gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash`) and **OpenAI** (`gpt-4o-mini`, `gpt-4o`) with automatic model-routing and optional cross-provider error fallback.
- **🌊 Real-Time Token Streaming:** Live typewriter-style content generation powered by Streamlit's `st.write_stream`.
- **📚 Personal Document Archive:** Persistent SQLite database with keyword search, category filtering, live in-app editing, and metrics tracking.
- **📥 Publication-Ready Exporters:** Instant 1-click downloads for styled Microsoft Word (`.docx`), styled PDF (`.pdf` via ReportLab), Markdown (`.md`), and Plain Text (`.txt`).

---

## 📁 Project Directory Structure

```text
Ai_writemate/
├── .streamlit/
│   └── config.toml          # Lavender theme and server configuration
├── ai/
│   ├── __init__.py          # Unified AI service package exports
│   ├── ai_service.py        # Central LLM facade, routing & fallback logic
│   ├── gemini_client.py     # Google Gemini API client (google-genai SDK)
│   └── openai_client.py     # OpenAI API client (openai>=1.0.0 SDK)
├── config/
│   └── __init__.py          # App configuration package
├── database/
│   ├── __init__.py          # Database package exports
│   ├── auth.py              # bcrypt password hashing & authentication logic
│   ├── db.py                # SQLite connection pool, transactions, & init_db
│   ├── models.py            # SQLite table schemas & Python dataclasses
│   └── writemate.db         # Local SQLite database (created on first run)
├── modules/
│   ├── __init__.py          # Core modules package exports
│   ├── exporter.py          # DOCX (python-docx) & PDF (ReportLab) generators
│   ├── grammar.py           # Grammar checking & proofreading engine
│   ├── history.py           # Document CRUD & user activity metrics
│   ├── rewriter.py          # Paraphrasing, tone shifting & simplification
│   ├── summarizer.py        # Bullet points, executive summaries, & TL;DR
│   └── writing.py           # Blog, email, code, and social drafting orchestrator
├── pages/
│   ├── dashboard.py         # Writing analytics, output charts & fast shortcuts
│   ├── history.py           # Document library, keyword search & live editor
│   ├── settings.py          # API key management, default models & security
│   └── writing_studio.py    # Main creation studio (Blog, Email, Code, Social)
├── prompts/
│   ├── __init__.py          # Reusable prompts package exports
│   ├── blog_prompts.py      # SEO article, outline, and headline builders
│   ├── code_prompts.py      # Code walkthrough, review, and debug templates
│   ├── email_prompts.py     # Executive, B2B cold outreach, and reply templates
│   ├── general_prompts.py   # Proofreading, summarization, and tone builders
│   └── social_prompts.py    # LinkedIn, Twitter threads, and Instagram templates
├── tests/
│   ├── __init__.py          # Test suite package
│   ├── test_ai_service.py   # AI provider resolution and routing tests
│   ├── test_auth.py         # bcrypt hashing, validation, & login tests
│   ├── test_database.py     # Database schema, foreign keys, & model tests
│   ├── test_exporter.py     # Word (.docx) & PDF (.pdf) export binary tests
│   └── test_prompts.py      # Prompt builder parameter verification tests
├── utils/
│   ├── __init__.py          # Utilities package
│   └── ui.py                # Lavender CSS injection & auth guard helpers
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore patterns
├── README.md                # Project documentation
└── requirements.txt         # Project dependencies
```

---

## 🚀 Local Setup & Installation

### 1. Prerequisites
- **Python 3.10+** installed
- Git (optional)

### 2. Clone or Navigate to the Project Directory
```powershell
cd "c:\Users\user\OneDrive\Desktop\Ai_writemate"
```

### 3. Create and Activate a Virtual Environment

#### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure API Keys
Copy the example environment template to `.env`:

#### On Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

#### On macOS / Linux:
```bash
cp .env.example .env
```

Open `.env` in an editor and insert your API keys:
```env
# AI Model Provider Keys
GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
OPENAI_API_KEY=sk-YourOpenAIApiKeyHere

# Default Model Selection
DEFAULT_MODEL=gemini-1.5-flash
DEFAULT_TEMPERATURE=0.7
```
*(Note: You only need at least one API key configured to use that provider. Keys can also be updated directly in the app's Settings page).*

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`. Register your user account to begin writing!

---

## 🧪 Running the Test Suite

Run the full automated test suite using `pytest`:

```bash
# Run all tests
pytest tests/ -v

# Run a specific test suite
pytest tests/test_auth.py -v
pytest tests/test_prompts.py -v
pytest tests/test_exporter.py -v
pytest tests/test_database.py -v
```

---

## ☁️ Deploying to Streamlit Community Cloud

Streamlit Community Cloud is a free, official platform to deploy Streamlit apps directly from your GitHub repository.

### Step 1: Push Code to GitHub
1. Initialize git and commit your files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of AI WriteMate"
   ```
2. Create a new repository on [GitHub](https://github.com) (e.g. `ai-writemate`).
3. Link and push your repository:
   ```bash
   git remote add origin https://github.com/<your-username>/ai-writemate.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud
1. Sign in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
2. Click **"New app"**.
3. Select your repository: `ai-writemate`, branch: `main`, and main file path: `app.py`.
4. Click **"Deploy!"**.

### Step 3: Configure Cloud Secrets
Do **not** commit your `.env` file to GitHub (it is ignored by `.gitignore`). Instead:
1. In your Streamlit Cloud app dashboard, click **Settings (gear icon) > Secrets**.
2. Paste your secret keys in TOML format:
   ```toml
   GEMINI_API_KEY = "AIzaSyYourActualGeminiKey"
   OPENAI_API_KEY = "sk-YourActualOpenAIKey"
   ```
3. Click **Save**. Streamlit will automatically restart the app with these environment variables accessible.

---

## ⚠️ Important Note on SQLite Persistence on Cloud Hosts

Streamlit Community Cloud runs apps inside **ephemeral Docker containers**:

> [!WARNING]
> Whenever an app on Streamlit Community Cloud sleeps due to inactivity, restarts, or pulls a new git commit, **its local container filesystem is reset**. Any changes made to a local SQLite database (`writemate.db`) during that session will be reverted to the state committed to git.

### Recommended Production Storage Solutions:
If you need permanent, persistent storage for multi-user cloud deployments:
1. **Serverless PostgreSQL (Recommended & Free):**
   - Connect to a free cloud PostgreSQL database like [Supabase](https://supabase.com) or [Neon](https://neon.tech).
   - In `database/db.py`, change `sqlite3` to `psycopg2` or `SQLAlchemy` with your PostgreSQL connection URI.
2. **Edge-Synced Cloud SQLite (Turso):**
   - [Turso](https://turso.tech) (built on `libsql`) allows you to keep an SQLite API while syncing all database writes to a persistent distributed database over HTTPS/WebSocket.
3. **Local Deployment / Persistent VPS:**
   - On local desktop environments, Docker with volume mounts, AWS EC2, DigitalOcean, or Railway, SQLite files remain 100% persistent on disk without any changes needed.
#   A i - w r i t e m a t e  
 #   A i - w r i t e m a t e  
 #   A i - w r i t e m a t e  
 