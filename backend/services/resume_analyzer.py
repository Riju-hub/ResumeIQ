import logging
from typing import Any, Dict, Optional

import spacy
from sentence_transformers import SentenceTransformer

from backend.services.groq_parser import parse_job_description, parse_resume
from backend.services.ats_scorer import (
    calculate_overall_score,
    detect_location_info,
    generate_critical_issues,
    generate_improvements,
    generate_strengths,
    validate_skills_with_projects,
)
from backend.services.jd_matcher import compare_resume_with_jd

logger = logging.getLogger("ats_resume_scorer")


def analyze_full_resume(
    resume_text: str,
    nlp: spacy.Language,
    embedder: SentenceTransformer,
    job_description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main orchestrator that parses the resume with Groq LLM, runs local NLP
    scoring (structure, skill validation, ATS privacy), compares with JD
    if provided, and builds the unified analysis dictionary.
    """
    logger.info("Step 1: Parsing resume with Groq LLM...")
    parsed_resume = parse_resume(resume_text)

    skills = parsed_resume.get("skills", [])
    keywords = parsed_resume.get("keywords", [])
    action_verbs = parsed_resume.get("action_verbs", [])
    projects = parsed_resume.get("projects", [])
    experience = parsed_resume.get("experience", [])

    exp_months = sum(
        e.get("duration_months", 0) for e in experience if isinstance(e, dict)
    )

    logger.info("Step 2: Checking privacy & location formatting...")
    location_results = detect_location_info(resume_text, nlp)

    logger.info("Step 3: Validating skills against projects/experience...")
    skill_val_results = validate_skills_with_projects(
        skills=skills,
        projects=projects,
        experience_entries=experience,
        embedder=embedder,
    )

    jd_comparison = None
    jd_keywords = []

    if job_description and job_description.strip():
        logger.info("Step 4: Parsing Job Description and running semantic matching...")
        try:
            jd_parsed = parse_job_description(job_description)
            jd_keywords = jd_parsed.get("keywords", []) + jd_parsed.get("required_skills", [])
            jd_comparison = compare_resume_with_jd(
                resume_text=resume_text,
                resume_keywords=keywords,
                resume_skills=skills,
                jd_text=job_description,
                jd_keywords=jd_keywords,
                embedder=embedder,
                nlp=nlp,
            )
        except Exception as exc:
            logger.warning(f"JD comparison failed, continuing with base scoring: {exc}")

    grammar_results = {"penalty_applied": 0.0, "total_errors": 0, "critical_errors": []}

    logger.info("Step 5: Calculating overall score components...")
    scores = calculate_overall_score(
        text=resume_text,
        parsed_resume=parsed_resume,
        skills=skills,
        keywords=keywords,
        action_verbs=action_verbs,
        skill_validation_results=skill_val_results,
        grammar_results=grammar_results,
        location_results=location_results,
        jd_keywords=jd_keywords if jd_keywords else None,
        experience_months=exp_months,
    )

    strengths = generate_strengths(scores, skill_val_results, grammar_results)
    issues = generate_critical_issues(scores, grammar_results, location_results)
    improvements = generate_improvements(scores, skill_val_results)

    raw_validated = skill_val_results.get("validated_skills", [])
    validated_dicts = []
    for item in raw_validated:
        if isinstance(item, dict):
            validated_dicts.append({
                "skill": item.get("skill", ""),
                "projects": item.get("projects", []),
                "similarity": float(item.get("similarity", 1.0)),
            })
        else:
            validated_dicts.append({
                "skill": str(item),
                "projects": [],
                "similarity": 1.0,
            })

    unvalidated_list = [
        item if isinstance(item, str) else item.get("skill", "")
        for item in skill_val_results.get("unvalidated_skills", [])
    ]

    return {
        "ats_score": scores["overall_score"],
        "component_scores": {
            "formatting": scores["formatting_score"],
            "keywords": scores["keywords_score"],
            "content": scores["content_score"],
            "skill_validation": scores["skill_validation_score"],
            "ats_compatibility": scores["ats_compatibility_score"],
        },
        "issues_summary": issues,
        "detailed_feedback": improvements,
        "strengths": strengths,
        "critical_issues": issues,
        "suggestions": improvements,
        "jd_comparison": jd_comparison,
        "skill_validation_details": {
            "validated": validated_dicts,
            "unvalidated": unvalidated_list,
            "total": len(skills),
            "validated_count": len(validated_dicts),
            "validation_pct": round(float(skill_val_results.get("validation_percentage", 0.0) * 100), 1),
        },
        "matched_keywords": jd_comparison.get("matched_keywords", []) if jd_comparison else keywords[:15],
        "missing_keywords": jd_comparison.get("missing_keywords", []) if jd_comparison else [],
        "skills": skills,
        "interpretation": scores.get("overall_interpretation", ""),
        "parsed_resume": parsed_resume,
    }