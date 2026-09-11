import os
from typing import Any, Dict, List
import requests
import streamlit as st

DEFAULT_BACKEND_URL = "http://localhost:8000"


def _backend_url() -> str:
    # 1. Check OS environment variable (used by Render / Docker / local shell)
    url = os.getenv("BACKEND_URL")
    if url:
        return url.rstrip("/")

    # 2. Check flat Streamlit secret: BACKEND_URL = "..."
    if hasattr(st, "secrets") and "BACKEND_URL" in st.secrets:
        return str(st.secrets["BACKEND_URL"]).rstrip("/")

    # 3. Check nested Streamlit secret: [backend] url = "..."
    if hasattr(st, "secrets") and "backend" in st.secrets and "url" in st.secrets["backend"]:
        return str(st.secrets["backend"]["url"]).rstrip("/")

    # 4. Fallback to default localhost
    return DEFAULT_BACKEND_URL


def _auth_headers(access_token: str) -> Dict[str, str]:
    if not access_token:
        return {}
    return {"Authorization": f"Bearer {access_token}"}


def health_check() -> Dict[str, Any]:
    url = f"{_backend_url()}/api/v1/health"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()


def analyze_resume(
    resume_file,
    access_token: str,
    job_description: str = "",
) -> Dict[str, Any]:
    # FastAPI expects UploadFile parameter named 'file' or 'resume'
    # Ensure parameter name matches routes.py (usually 'file' or 'resume')
    files = {
        "file": (resume_file.name, resume_file.getvalue(), resume_file.type or "application/pdf"),
    }
    data = {"job_description": job_description}
    headers = _auth_headers(access_token)

    response = requests.post(
        f"{_backend_url()}/api/v1/analyze-resume",
        files=files,
        data=data,
        headers=headers,
        timeout=(20, 240),  # 20s connect, 240s processing for LLM + NLP
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


def generate_pdf(analysis_data: Dict[str, Any], access_token: str) -> bytes:
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