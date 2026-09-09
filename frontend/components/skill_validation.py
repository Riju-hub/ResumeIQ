from typing import Any, Dict
import streamlit as st

def display_skill_validation(analysis: Dict[str, Any]) -> None:
    details = analysis.get("skill_validation_details") or {}
    validated = details.get("validated", [])
    unvalidated = details.get("unvalidated", [])
    total = details.get("total", len(validated) + len(unvalidated))
    pct = details.get("validation_pct", 0.0)

    st.markdown("### 🔍 Skill Demonstration Matrix")

    if total == 0:
        st.info("No extracted technical skills found in resume.")
        return

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Skills Detected", total)
    m2.metric("Evidence-Validated", len(validated))
    m3.metric("Verification Rate", f"{pct:.0f}%")

    if validated:
        with st.expander(f"✅ Demonstrated Skills ({len(validated)})", expanded=True):
            chips_html = "".join([
                f"<span style='display:inline-block; background:#ECFDF5; border:1px solid #A7F3D0; color:#065F46; padding:4px 10px; border-radius:6px; font-size:0.85rem; margin:3px;'>✓ {v.get('skill', '?')}</span>"
                for v in validated
            ])
            st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)

    if unvalidated:
        with st.expander(f"⚠️ Unsubstantiated Claims ({len(unvalidated)})", expanded=False):
            chips_html = "".join([
                f"<span style='display:inline-block; background:#FFF1F2; border:1px solid #FECDD3; color:#991B1B; padding:4px 10px; border-radius:6px; font-size:0.85rem; margin:3px;'>! {s}</span>"
                for s in unvalidated
            ])
            st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)
            st.caption("These skills were listed in your summary/skills list but are not evidenced inside project/work bullet points.")