from typing import Any, Dict, Optional
import streamlit as st

def display_jd_comparison(jd_comparison: Optional[Dict[str, Any]]) -> None:
    if not jd_comparison:
        return

    st.markdown("### 🎯 Job Description Alignment")

    match_pct = float(jd_comparison.get("match_percentage", 0))
    semantic = float(jd_comparison.get("semantic_similarity", 0))
    matched = jd_comparison.get("matched_keywords", []) or []
    missing = jd_comparison.get("missing_keywords", []) or []

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Overall Match Score", f"{match_pct:.0f}%")
        st.progress(min(max(match_pct / 100.0, 0.0), 1.0))
    with c2:
        st.metric("Semantic Similarity", f"{semantic * 100:.0f}%")
        st.progress(min(max(semantic, 0.0), 1.0))

    k1, k2 = st.columns(2)
    with k1:
        st.markdown("**✅ Matched Keywords**")
        if matched:
            matched_html = "".join([f"<span style='display:inline-block; background:#EFF6FF; border:1px solid #BFDBFE; color:#1E40AF; padding:3px 8px; border-radius:4px; font-size:0.8rem; margin:2px;'>{kw}</span>" for kw in matched[:20]])
            st.markdown(matched_html, unsafe_allow_html=True)
        else:
            st.caption("No direct keyword matches found.")
    with k2:
        st.markdown("**❌ Missing High-Priority Keywords**")
        if missing:
            missing_html = "".join([f"<span style='display:inline-block; background:#FFF1F2; border:1px solid #FECDD3; color:#991B1B; padding:3px 8px; border-radius:4px; font-size:0.8rem; margin:2px;'>{kw}</span>" for kw in missing[:20]])
            st.markdown(missing_html, unsafe_allow_html=True)
        else:
            st.caption("All primary requirements matched.")