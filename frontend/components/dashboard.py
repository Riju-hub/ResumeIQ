from typing import Any, Dict
import requests
import streamlit as st

from frontend.services import api_client
from frontend.components.score_display import display_overall_score, display_score_breakdown
from frontend.components.strengths_issues import display_strengths, display_critical_issues
from frontend.components.skill_validation import display_skill_validation
from frontend.components.jd_comparison import display_jd_comparison
from frontend.components.detailed_feedback import display_detailed_feedback
from frontend.components.action_items import display_action_items
from frontend.components.recommendations import display_recommendations


def inject_dashboard_css():
    """Inject modern styling, ambient multi-color mesh, and responsive mobile rules."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@600;700&display=swap');

            /* --- 1. Global Multi-Color Ambient Mesh Canvas --- */
            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stHeader"] {
                background: 
                    radial-gradient(ellipse 65% 55% at 5% 5%, rgba(99, 102, 241, 0.12) 0%, transparent 60%),
                    radial-gradient(ellipse 55% 50% at 95% 10%, rgba(14, 165, 233, 0.10) 0%, transparent 60%),
                    radial-gradient(ellipse 60% 55% at 90% 90%, rgba(236, 72, 153, 0.08) 0%, transparent 60%),
                    radial-gradient(ellipse 50% 50% at 10% 95%, rgba(16, 185, 129, 0.08) 0%, transparent 60%),
                    radial-gradient(ellipse 70% 60% at 50% 50%, rgba(139, 92, 246, 0.06) 0%, transparent 70%),
                    #f8fafc !important;
                background-attachment: fixed !important;
            }

            header[data-testid="stHeader"] {
                background: transparent !important;
            }

            /* --- 2. Container & Geometry --- */
            .dashboard-scope, .dashboard-scope * {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
                box-sizing: border-box !important;
            }

            .dashboard-scope {
                width: 100%;
                max-width: 1180px;
                margin: 0 auto;
                padding: 0 4px;
            }

            /* --- 3. Sleek Deliverables Card --- */
            .export-card-glow {
                background: rgba(255, 255, 255, 0.85) !important;
                backdrop-filter: blur(14px) !important;
                -webkit-backdrop-filter: blur(14px) !important;
                border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
                border-radius: 20px;
                padding: clamp(18px, 3vw, 26px);
                margin: 2.2rem 0 1.2rem 0;
                box-shadow: 0 16px 36px -10px rgba(99, 102, 241, 0.15), 0 0 20px -5px rgba(236, 72, 153, 0.1);
                position: relative;
                overflow: hidden;
            }

            .export-card-glow::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #4f46e5 0%, #0ea5e9 33%, #ec4899 66%, #10b981 100%);
            }

            .export-tag {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 12px;
                border-radius: 9999px;
                background: rgba(99, 102, 241, 0.1);
                border: 1px solid rgba(99, 102, 241, 0.25);
                color: #4f46e5;
                font-size: 0.72rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: 8px;
            }

            .export-main-title {
                color: #0f172a;
                font-size: clamp(1.15rem, 2.5vw, 1.45rem);
                font-weight: 800;
                letter-spacing: -0.02em;
                margin: 0 0 4px 0;
            }

            .export-desc {
                color: #475569;
                font-size: clamp(0.84rem, 1.8vw, 0.92rem);
                line-height: 1.5;
                margin: 0;
            }

            .glass-divider {
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(203, 213, 225, 0.9), transparent);
                margin: 1.6rem 0;
                border: 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _summary_text(analysis: Dict[str, Any]) -> str:
    """Generates a complete, comprehensive plaintext summary matching the full dashboard."""
    if not isinstance(analysis, dict):
        return str(analysis)

    lines = [
        "=" * 60,
        "                ATS RESUME ANALYSIS REPORT                  ",
        "=" * 60,
        "",
    ]

    # 1. Overall Score & Verdict
    raw_score = analysis.get("ATS_score", analysis.get("ats_score", analysis.get("overall_score", 0.0)))
    try:
        score = round(float(raw_score), 1)
    except Exception:
        score = 0.0

    lines.append(f"OVERALL ATS SCORE: {score}/100")
    if analysis.get("interpretation"):
        lines.append(f"Verdict: {analysis['interpretation']}")
    lines.append("-" * 60 + "\n")

    # 2. Score Breakdown
    comp_scores = analysis.get("component_scores")
    if hasattr(comp_scores, "model_dump"):
        comp_scores = comp_scores.model_dump()
    if isinstance(comp_scores, dict):
        lines.append("📈 SCORE BREAKDOWN:")
        for comp, val in comp_scores.items():
            lines.append(f"  • {comp.replace('_', ' ').title()}: {val}")
        lines.append("")

    # 3. Strengths & Critical Blockers
    strengths = analysis.get("strengths") or []
    if strengths:
        lines.append("💪 IDENTIFIED STRENGTHS:")
        for s in strengths:
            lines.append(f"  ✓ {s}")
        lines.append("")

    # 4. Job Description Match (If Present)
    jd_comp = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    if hasattr(jd_comp, "model_dump"):
        jd_comp = jd_comp.model_dump()
    if isinstance(jd_comp, dict) and jd_comp:
        lines.append("🎯 JOB DESCRIPTION MATCH:")
        lines.append(f"  • Match Percentage: {jd_comp.get('match_percentage', 0)}%")
        lines.append(f"  • Semantic Similarity: {jd_comp.get('semantic_similarity', 0)}")
        matched_kw = jd_comp.get("matched_keywords") or []
        missing_kw = jd_comp.get("missing_keywords") or []
        if matched_kw:
            lines.append(f"  • Matched Keywords: {', '.join(str(k) for k in matched_kw[:15])}")
        if missing_kw:
            lines.append(f"  • Missing Keywords: {', '.join(str(k) for k in missing_kw[:15])}")
        lines.append("")

    # 5. Skill Demonstration Matrix
    val_details = analysis.get("skill_validation_details")
    if hasattr(val_details, "model_dump"):
        val_details = val_details.model_dump()
    if isinstance(val_details, dict):
        total = val_details.get("total", 0)
        valid_cnt = val_details.get("validated_count", len(val_details.get("validated", [])))
        pct = val_details.get("validation_pct", 0)
        lines.append("🔍 SKILL DEMONSTRATION MATRIX:")
        lines.append(f"  • Total Skills Detected: {total}")
        lines.append(f"  • Evidence-Validated: {valid_cnt}")
        lines.append(f"  • Verification Rate: {pct}%\n")

    lines.append("=" * 60)
    return "\n".join(lines)


def _render_export_section(analysis: Dict[str, Any]) -> None:
    """Renders the modern glassmorphism export card with PDF & plain text generators."""
    st.markdown(
        """
        <div class="export-card-glow">
            <span class="export-tag">⚡ Deliverables</span>
            <div class="export-main-title">Export Audit Summary & PDF Report</div>
            <p class="export-desc">Download complete diagnostics, keyword gap benchmarks, and remediation checklists.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="medium")

    with c1:
        if st.button("📑 Generate Official PDF", use_container_width=True, type="primary", key="dashboard_gen_pdf_btn"):
            token = st.session_state.get("access_token", "")
            try:
                with st.spinner("Compiling high-resolution report..."):
                    pdf_bytes = api_client.generate_pdf(analysis, access_token=token)
                    st.session_state["dashboard_pdf_bytes"] = pdf_bytes
                    st.toast("PDF successfully compiled!", icon="📄")
            except requests.RequestException as exc:
                st.error(f"Failed to generate PDF: {exc}")

        if "dashboard_pdf_bytes" in st.session_state and st.session_state["dashboard_pdf_bytes"]:
            st.download_button(
                label="⬇️ Download PDF Report",
                data=st.session_state["dashboard_pdf_bytes"],
                file_name="ATS_Resume_Analysis_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="dashboard_download_pdf_btn",
            )

    with c2:
        st.download_button(
            label="📄 Download Summary (.txt)",
            data=_summary_text(analysis),
            file_name="ATS_Analysis_Summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="dashboard_download_txt_btn",
        )


def display_results_dashboard(analysis: Dict[str, Any]) -> None:
    """Renders the complete evaluation dashboard inside an adaptive, modern container."""
    inject_dashboard_css()

    st.markdown('<div class="dashboard-scope">', unsafe_allow_html=True)

    # 1. Score Overview & Dimensional Breakdown
    display_overall_score(analysis)
    display_score_breakdown(analysis)

    st.markdown("<div class='glass-divider'></div>", unsafe_allow_html=True)

    # 2. Strengths vs Critical Flaws
    col_s, col_i = st.columns(2, gap="large")
    with col_s:
        display_strengths(analysis.get("strengths") or [])
    with col_i:
        display_critical_issues(analysis)

    # 3. Contextual Job Description Match (Conditional)
    jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    if jd_comparison:
        st.markdown("<div class='glass-divider'></div>", unsafe_allow_html=True)
        display_jd_comparison(jd_comparison)

    st.markdown("<div class='glass-divider'></div>", unsafe_allow_html=True)

    # 4. Skill Demonstration & Verification Matrix
    display_skill_validation(analysis)

    st.markdown("<div class='glass-divider'></div>", unsafe_allow_html=True)

    # 5. Granular Feedback & Actionable Roadmap
    display_detailed_feedback(analysis)
    display_action_items(analysis)

    try:
        if analysis.get("recommendations"):
            display_recommendations(analysis)
    except Exception:
        pass

    # 6. Export Options
    _render_export_section(analysis)

    st.markdown('</div>', unsafe_allow_html=True)