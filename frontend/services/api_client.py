import os
from typing import Any, Dict, List, Optional
import requests
import streamlit as st

PROD_BACKEND_URL = "https://resumeiq-backend-awry.onrender.com"
# PROD_BACKEND_URL = "localhost:8000"  # For local development

def _backend_url() -> str:
    """Resolves the backend URL across secrets, env vars, and production fallback."""
    # 1. Check Streamlit secrets (flat or nested)
    if hasattr(st, "secrets"):
        if "BACKEND_URL" in st.secrets and st.secrets["BACKEND_URL"]:
            return str(st.secrets["BACKEND_URL"]).strip().rstrip("/")
        if "backend" in st.secrets and "url" in st.secrets["backend"]:
            return str(st.secrets["backend"]["url"]).strip().rstrip("/")

    # 2. Check OS environment variable
    env_url = os.getenv("BACKEND_URL", "").strip()
    if env_url:
        return env_url.rstrip("/")

    # 3. Cloud / Local fallback
    return PROD_BACKEND_URL


def _auth_headers(access_token: Optional[str]) -> Dict[str, str]:
    if not access_token:
        return {}
    return {"Authorization": f"Bearer {access_token}"}


def health_check() -> Dict[str, Any]:
    try:
        url = f"{_backend_url()}/api/v1/health"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"status": "unhealthy", "code": response.status_code}
    except Exception as exc:
        return {"status": "offline", "error": str(exc)}


def analyze_resume(
    resume_file,
    access_token: Optional[str] = None,
    job_description: str = "",
) -> Dict[str, Any]:
    files = {
        "resume": (resume_file.name, resume_file.getvalue(), resume_file.type or "application/pdf"),
    }
    data = {"job_description": job_description}
    headers = _auth_headers(access_token)

    url = f"{_backend_url()}/api/v1/analyze-resume"
    response = requests.post(
        url,
        files=files,
        data=data,
        headers=headers,
        timeout=(20, 240),
    )
    response.raise_for_status()
    return response.json()


def get_history(access_token: str) -> List[Dict[str, Any]]:
    response = requests.get(
        f"{_backend_url()}/api/v1/history",
        headers=_auth_headers(access_token),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def delete_history_entry(analysis_id: str, access_token: str) -> None:
    response = requests.delete(
        f"{_backend_url()}/api/v1/history/{analysis_id}",
        headers=_auth_headers(access_token),
        timeout=30,
    )
    response.raise_for_status()


def generate_pdf(analysis_data: Dict[str, Any], access_token: Optional[str] = None) -> bytes:
    response = requests.post(
        f"{_backend_url()}/api/v1/generate-pdf",
        json=analysis_data,
        headers=_auth_headers(access_token),
        timeout=(15, 180),
    )
    response.raise_for_status()
    return response.content


def get_history_pdf(analysis_id: str, access_token: str) -> bytes:
    response = requests.get(
        f"{_backend_url()}/api/v1/history/{analysis_id}/pdf",
        headers=_auth_headers(access_token),
        timeout=(15, 180),
    )
    response.raise_for_status()
    return response.content