from typing import Any, Dict, List, Union

import streamlit as st

from frontend.components._helpers import get_severity_style


SEVERITY_ORDER = ["critical", "high", "medium", "low"]


def _normalize_issue(issue: Union[Dict[str, Any], str, Any]) -> Dict[str, Any]:
    """Converts dictionaries, Pydantic models, or raw strings into a uniform dict."""
    if isinstance(issue, str):
        return {
            "issue_title": issue,
            "severity_level": "medium",
            "ats_impact": "Moderate impact on ATS matching",
            "explanation": issue,
            "where_it_appears": "General Resume Content",
            "how_to_fix": "Review the relevant section of your resume to address this point.",
            "action_items": [],
            "example_improvement": "",
        }

    # If it's a Pydantic model
    if hasattr(issue, "model_dump"):
        issue = issue.model_dump()
    elif hasattr(issue, "dict"):
        issue = issue.dict()

    if isinstance(issue, dict):
        return {
            "issue_title": issue.get("issue_title") or issue.get("title") or "Improvement Suggestion",
            "severity_level": str(issue.get("severity_level") or issue.get("severity") or "medium").lower(),
            "ats_impact": issue.get("ats_impact") or "Moderate",
            "explanation": issue.get("explanation") or "",
            "where_it_appears": issue.get("where_it_appears") or "",
            "how_to_fix": issue.get("how_to_fix") or "",
            "action_items": issue.get("action_items") or [],
            "example_improvement": issue.get("example_improvement") or "",
        }

    return {
        "issue_title": str(issue),
        "severity_level": "medium",
        "ats_impact": "Noticeable",
        "explanation": str(issue),
        "where_it_appears": "General",
        "how_to_fix": "Review and update this section.",
        "action_items": [],
        "example_improvement": "",
    }


def _group_by_severity(issues: List[Union[Dict[str, Any], str]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {level: [] for level in SEVERITY_ORDER}

    for item in issues:
        norm_issue = _normalize_issue(item)
        level = norm_issue.get("severity_level", "medium")
        if level not in grouped:
            level = "medium"
        grouped[level].append(norm_issue)

    return grouped


def _render_issue(issue: Dict[str, Any]) -> None:
    icon, text_color, bg_color = get_severity_style(issue.get("severity_level"))
    title = issue.get("issue_title", "Untitled issue")
    impact = issue.get("ats_impact", "")
    explanation = issue.get("explanation", "")
    where = issue.get("where_it_appears", "")
    how_to_fix = issue.get("how_to_fix", "")
    action_items = issue.get("action_items") or []
    example = issue.get("example_improvement", "")

    st.markdown(
        f"""
        <div style="border-left:4px solid {text_color}; background-color:{bg_color};
                    padding:0.75rem 1rem; border-radius:6px; margin-bottom:0.5rem;">
            <strong style="color:{text_color};">{icon} {title}</strong>
            <span style="color:#666; margin-left:0.5rem; font-size:0.85rem;">{impact}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Details", expanded=False):
        if explanation:
            st.markdown(f"**What's happening:** {explanation}")
        if where:
            st.markdown(f"**Where it appears:** {where}")
        if how_to_fix:
            st.markdown(f"**How to fix:** {how_to_fix}")
        if action_items:
            st.markdown("**Action items:**")
            for item in action_items:
                st.markdown(f"- {item}")
        if example:
            st.markdown("**Example improvement:**")
            st.code(example, language="text")


def display_detailed_feedback(analysis: Dict[str, Any]) -> None:
    issues = analysis.get("detailed_feedback") or []
    if not issues:
        return

    st.markdown("### 🔍 Detailed Feedback")
    st.caption(f"{len(issues)} issue(s) flagged — grouped by severity.")

    grouped = _group_by_severity(issues)
    for level in SEVERITY_ORDER:
        items = grouped.get(level, [])
        if not items:
            continue
        st.markdown(f"#### {level.title()} ({len(items)})")
        for issue in items:
            _render_issue(issue)