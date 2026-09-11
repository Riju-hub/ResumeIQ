import json
import logging
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logger = logging.getLogger('ats_resume_scorer')

_client: Optional[Groq] = None
_resolved_model: Optional[str] = None

# Active models available on your Groq key
AVAILABLE_CHAT_MODELS: List[str] = [
    'openai/gpt-oss-120b',
    'qwen/qwen3.8-27b',
    'openai/gpt-oss-20b',
    'qwen/qwen3.6-27b',
]


def _get_client() -> Groq:
    global _client
    if _client is None:
        load_dotenv()
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set. Please check your .env file.")
        _client = Groq(api_key=api_key, timeout=30.0)
    return _client


def _get_active_model(client: Groq) -> str:
    global _resolved_model
    if _resolved_model:
        return _resolved_model

    env_model = os.getenv('GROQ_MODEL')
    try:
        models_data = client.models.list().data
        available_ids = {m.id for m in models_data}

        if env_model and env_model in available_ids:
            _resolved_model = env_model
            return _resolved_model

        for candidate in AVAILABLE_CHAT_MODELS:
            if candidate in available_ids:
                _resolved_model = candidate
                logger.info(f"Using verified Groq model: {_resolved_model}")
                return _resolved_model

        # Fallback to the first non-whisper/non-guard model
        for mid in available_ids:
            if not any(k in mid.lower() for k in ['whisper', 'guard', 'orpheus']):
                _resolved_model = mid
                return _resolved_model

        _resolved_model = 'openai/gpt-oss-120b'
        return _resolved_model
    except Exception as exc:
        logger.warning(f"Error checking models ({exc}), defaulting to openai/gpt-oss-120b")
        return 'openai/gpt-oss-120b'


RESUME_SYSTEM_PROMPT = (
    "You are a strict resume parser. Extract structured information from the resume "
    "and return ONLY a valid JSON object matching the requested schema."
)

RESUME_USER_PROMPT = """Extract the following information from this resume into valid JSON:
{{
  "name": "full name",
  "email": "email address or null",
  "phone": "phone number or null",
  "linkedin": "LinkedIn URL or null",
  "github": "GitHub URL or null",
  "professional_summary": "Summary, Profile, or Objective text, or empty string",
  "skills": ["list", "of", "skills"],
  "experience": [
    {{
      "job_title": "title",
      "company": "company",
      "start_date": "start",
      "end_date": "end",
      "duration_months": 0,
      "description": "brief summary of role"
    }}
  ],
  "education": [
    {{
      "degree": "degree",
      "institution": "school or university",
      "year": "year"
    }}
  ],
  "certifications": ["list of certifications"],
  "projects": [
    {{
      "title": "project name",
      "description": "what was built and how",
      "technologies": ["tech", "used"]
    }}
  ],
  "action_verbs": ["strong action verbs, e.g. built, developed, architected"],
  "keywords": ["key domain terms, tech stack, and ATS keywords"]
}}

Resume Text:
{raw_text}"""

JD_SYSTEM_PROMPT = (
    "You are a strict job description parser. Extract information "
    "and return ONLY a valid JSON object matching the requested schema."
)

JD_USER_PROMPT = """Extract the following from this job description into valid JSON:
{{
  "job_title": "job title",
  "required_skills": ["list of must-have skills"],
  "preferred_skills": ["list of nice-to-have skills"],
  "experience_required": "experience requirements",
  "education_required": "education requirements",
  "key_responsibilities": ["key responsibilities"],
  "keywords": ["important keywords for ATS matching"]
}}

Job Description Text:
{raw_text}"""


def _call_groq_json(client: Groq, system_prompt: str, user_prompt: str, max_tokens: int = 2048) -> str:
    model_name = _get_active_model(client)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        temperature=0.1,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
        timeout=30.0
    )
    return response.choices[0].message.content.strip()


def _try_parse_json(text: str) -> dict | None:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        first_newline = cleaned.index("\n") if "\n" in cleaned else len(cleaned)
        cleaned = cleaned[first_newline + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def parse_resume(raw_text: str) -> Dict:
    client = _get_client()
    prompt = RESUME_USER_PROMPT.format(raw_text=raw_text[:6500])

    try:
        raw_response = _call_groq_json(client, RESUME_SYSTEM_PROMPT, prompt, max_tokens=2048)
        result = _try_parse_json(raw_response)
        if result is not None:
            return _validate_resume_result(result)
    except Exception as e:
        logger.warning(f"Groq primary resume parse attempt failed: {e}")

    logger.warning("Groq resume parse: retrying with concise prompt...")
    strict_prompt = prompt + "\n\nCRITICAL: Keep descriptions brief to ensure the JSON does not truncate."
    raw_response = _call_groq_json(client, RESUME_SYSTEM_PROMPT, strict_prompt, max_tokens=1024)
    result = _try_parse_json(raw_response)

    if result is not None:
        return _validate_resume_result(result)

    raise ValueError(f"Groq returned unparseable response: {raw_response[:300]}")


def parse_job_description(raw_text: str) -> Dict:
    client = _get_client()
    prompt = JD_USER_PROMPT.format(raw_text=raw_text[:4500])

    try:
        raw_response = _call_groq_json(client, JD_SYSTEM_PROMPT, prompt, max_tokens=1500)
        result = _try_parse_json(raw_response)
        if result is not None:
            return _validate_jd_result(result)
    except Exception as e:
        logger.warning(f"Groq JD parse attempt failed: {e}")

    strict_prompt = prompt + "\n\nCRITICAL: Keep output concise and return valid JSON."
    raw_response = _call_groq_json(client, JD_SYSTEM_PROMPT, strict_prompt, max_tokens=800)
    result = _try_parse_json(raw_response)

    if result is not None:
        return _validate_jd_result(result)

    raise ValueError(f"Groq JD unparseable response: {raw_response[:300]}")


def _validate_jd_result(result: dict) -> dict:
    defaults = {
        "job_title": "",
        "required_skills": [],
        "preferred_skills": [],
        "experience_required": "",
        "education_required": "",
        "key_responsibilities": [],
        "keywords": [],
    }
    for key, default in defaults.items():
        if key not in result or result[key] is None:
            result[key] = default
        if isinstance(default, list) and not isinstance(result[key], list):
            result[key] = default
    return result


def _validate_resume_result(result: dict) -> dict:
    defaults = {
        "name": "",
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "professional_summary": "",
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": [],
        "projects": [],
        "action_verbs": [],
        "keywords": [],
    }
    for key, default in defaults.items():
        if key not in result or result[key] is None:
            result[key] = default
        if isinstance(default, list) and not isinstance(result[key], list):
            result[key] = default

    for exp in result.get("experience", []):
        if not isinstance(exp, dict):
            continue
        exp.setdefault("job_title", "")
        exp.setdefault("company", "")
        exp.setdefault("start_date", "")
        exp.setdefault("end_date", "")
        exp.setdefault("duration_months", 0)
        exp.setdefault("description", "")
        try:
            exp["duration_months"] = int(exp["duration_months"])
        except (ValueError, TypeError):
            exp["duration_months"] = 0

    for proj in result.get("projects", []):
        if not isinstance(proj, dict):
            continue
        proj.setdefault("title", "")
        proj.setdefault("description", "")
        proj.setdefault("technologies", [])

    return result