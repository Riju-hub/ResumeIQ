from typing import Any, Dict, List
import streamlit as st

def display_strengths(strengths: List[str]) -> None:
    st.markdown("### 💪 Strengths")
    if not strengths:
        st.info("Improve metrics and structure to unlock standout strengths.")
        return
    for item in strengths:
        st.markdown(
            f"""
            <div style="background:#ECFDF5; border-left:4px solid #10B981; padding:0.6rem 0.9rem; border-radius:6px; margin-bottom:0.4rem; font-size:0.9rem; color:#065F46;">
                ✓ {item}
            </div>
            """,
            unsafe_allow_html=True
        )

def display_critical_issues(analysis: Dict[str, Any]) -> None:
    critical = analysis.get("critical_issues") or []
    st.markdown("### 🚨 Critical Blockers")
    if not critical:
        st.markdown(
            """
            <div style="background:#ECFDF5; border:1px solid #A7F3D0; padding:1rem; border-radius:8px; color:#065F46;">
                <strong>🎉 No Critical Errors Found!</strong><br>
                <span style="font-size:0.85rem;">Your document complies cleanly with standard ATS parsing rules.</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    for item in critical:
        st.markdown(
            f"""
            <div style="background:#FFF1F2; border-left:4px solid #E11D48; padding:0.6rem 0.9rem; border-radius:6px; margin-bottom:0.4rem; font-size:0.9rem; color:#991B1B;">
                ✖ {item}
            </div>
            """,
            unsafe_allow_html=True
        )