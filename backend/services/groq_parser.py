import json
import logging
import os
from typing import Dict

from groq import Groq

logger = logging.getLogger('ats_resume_scorer')

# Use your active Groq model
GROQ_MODEL = 'openai/gpt-oss-120b'
_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        _client = Groq(api_key=api_key, timeout=30.0)
    return _client


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


def _call_groq_json(client: Groq, system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        temperature=0.1,
        max_tokens=4096,  # Increased token limit so long summaries/experience do not truncate
        response_format={"type": "json_object"},  # Enforces valid JSON from Groq engine
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
    prompt = RESUME_USER_PROMPT.format(raw_text=raw_text[:7000])

    try:
        raw_response = _call_groq_json(client, RESUME_SYSTEM_PROMPT, prompt)
        result = _try_parse_json(raw_response)
        if result is not None:
            return _validate_resume_result(result)
    except Exception as e:
        logger.warning(f"Groq primary resume parse attempt failed: {e}")

    # Fallback retry attempt
    logger.warning("Groq resume parse: retrying with strict prompt...")
    strict_prompt = prompt + "\n\nCRITICAL: Keep descriptions brief to ensure the JSON does not truncate."
    raw_response = _call_groq_json(client, RESUME_SYSTEM_PROMPT, strict_prompt)
    result = _try_parse_json(raw_response)

    if result is not None:
        return _validate_resume_result(result)

    raise ValueError(f"Groq returned unparseable response. Output: {raw_response[:300]}")


def parse_job_description(raw_text: str) -> Dict:
    client = _get_client()
    prompt = JD_USER_PROMPT.format(raw_text=raw_text[:5000])

    try:
        raw_response = _call_groq_json(client, JD_SYSTEM_PROMPT, prompt)
        result = _try_parse_json(raw_response)
        if result is not None:
            return _validate_jd_result(result)
    except Exception as e:
        logger.warning(f"Groq JD parse attempt failed: {e}")

    strict_prompt = prompt + "\n\nCRITICAL: Keep output concise and return valid JSON."
    raw_response = _call_groq_json(client, JD_SYSTEM_PROMPT, strict_prompt)
    result = _try_parse_json(raw_response)

    if result is not None:
        return _validate_jd_result(result)

    raise ValueError(f"Groq JD unparseable response. Output: {raw_response[:300]}")


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