import os
from pathlib import Path
from dotenv import load_dotenv

# Search current directory, parent (backend/), and grandparent (root) for .env
current_dir = Path(__file__).resolve().parent
for env_candidate in [
    current_dir / ".env",
    current_dir.parent / ".env",
    current_dir.parent.parent / ".env",
]:
    if env_candidate.exists():
        load_dotenv(env_candidate, override=True)

# API metadata
APP_TITLE = "ATS RESUME ANALYZER API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "analyse resumes against job description using nlp + ml"

# CORS origins (no trailing slashes)
ALLOWED_ORIGINS = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "https://appapppy-ktwxupi73vqhjzweksze9d.streamlit.app",
]

# File settings
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

SUPPORTED_MIME_TYPES = {
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}

SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx"}

SPACY_MODEL_PRIMARY = "en_core_web_md"
SPACY_MODEL_SECONDARY = "en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

# Score component weights
SCORE_WEIGHTS = {
    "formatting": 20,
    "keywords": 25,
    "content": 25,
    "skill_validation": 15,
    "ats_compatibility": 15,
}

JD_KEYWORD_WEIGHT = 0.6
JD_SEMANTIC_WEIGHT = 0.4

# Supabase & LLM credentials
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "").strip()
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()