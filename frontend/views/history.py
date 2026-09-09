from datetime import datetime
from typing import Any, Dict, List

import requests
import streamlit as st

from frontend.services import api_client


def inject_custom_css():
    """Inject corporate responsive styling with multi-color mesh background and glass ledger cards."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

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

            /* --- 2. Typography & Scope Containers --- */
            .history-scope, .history-scope * {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
                box-sizing: border-box !important;
            }

            .history-scope {
                width: 100%;
                max-width: 1180px;
                margin: 0 auto;
                padding: 0 4px;
            }

            .history-badge-pill {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 5px 14px;
                border-radius: 9999px;
                background: rgba(99, 102, 241, 0.12);
                border: 1px solid rgba(99, 102, 241, 0.3);
                color: #4f46e5;
                font-size: 0.76rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: 8px;
            }

            .history-main-title {
                color: #0f172a;
                font-size: clamp(1.6rem, 4vw, 2.5rem);
                font-weight: 900;
                letter-spacing: -0.03em;
                line-height: 1.2;
                margin: 0 0 6px 0;
            }

            .history-main-title span {
                background: linear-gradient(135deg, #4f46e5 0%, #0ea5e9 50%, #ec4899 100%);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .history-main-desc {
                color: #475569;
                font-size: clamp(0.88rem, 1.8vw, 1rem);
                line-height: 1.55;
                margin: 0 0 24px 0;
            }

            /* --- 3. Glassmorphic Summary KPI Cards --- */
            .stat-card-glow {
                background: rgba(255, 255, 255, 0.88) !important;
                backdrop-filter: blur(14px) !important;
                -webkit-backdrop-filter: blur(14px) !important;
                border: 1.5px solid rgba(226, 232, 240, 0.9) !important;
                border-radius: 18px;
                padding: clamp(16px, 2.5vw, 20px);
                margin-bottom: 14px;
                box-shadow: 0 6px 20px -6px rgba(15, 23, 42, 0.06);
                position: relative;
                overflow: hidden;
                transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
            }

            .stat-card-glow:hover {
                transform: translateY(-3px);
                border-color: rgba(99, 102, 241, 0.4) !important;
                box-shadow: 0 14px 28px -6px rgba(99, 102, 241, 0.15);
            }

            .stat-card-indigo { border-top: 3.5px solid #6366f1 !important; }
            .stat-card-cyan   { border-top: 3.5px solid #0ea5e9 !important; }
            .stat-card-emerald{ border-top: 3.5px solid #10b981 !important; }

            .stat-label-wrap {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.76rem;
                color: #64748b;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 6px;
            }

            .stat-value {
                font-size: clamp(1.4rem, 3vw, 1.85rem);
                font-weight: 900;
                color: #0f172a;
                letter-spacing: -0.02em;
            }

            /* --- 4. High-Contrast Status Pills --- */
            .score-pill-pro {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 12px;
                border-radius: 9999px;
                font-size: 0.8rem;
                font-weight: 800;
                letter-spacing: 0.02em;
                white-space: nowrap;
            }

            .pill-high { 
                background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                color: #047857;
                border: 1px solid #6ee7b7;
                box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
            }
            .pill-mid { 
                background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
                color: #b45309;
                border: 1px solid #fcd34d;
                box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
            }
            .pill-low { 
                background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
                color: #b91c1c;
                border: 1px solid #fca5a5;
                box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
            }

            /* --- 5. Dimension Metric Cards & Progress Bars --- */
            .metric-box-glass {
                background: rgba(248, 250, 252, 0.85) !important;
                border: 1px solid rgba(226, 232, 240, 0.95);
                border-radius: 12px;
                padding: 12px 14px;
                margin-bottom: 10px;
                box-shadow: 0 1px 3px rgba(15, 23, 42, 0.02);
            }

            .metric-box-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 6px;
            }

            .metric-box-title {
                font-size: 0.84rem;
                font-weight: 700;
                color: #334155;
            }

            .metric-box-val {
                font-size: 0.86rem;
                font-weight: 800;
                color: #0f172a;
            }

            .progress-track-pro {
                width: 100%;
                height: 7px;
                background: #e2e8f0;
                border-radius: 9999px;
                overflow: hidden;
            }

            .progress-fill-emerald {
                height: 100%;
                background: linear-gradient(90deg, #10b981, #059669);
                border-radius: 9999px;
            }

            .progress-fill-indigo {
                height: 100%;
                background: linear-gradient(90deg, #6366f1, #4f46e5);
                border-radius: 9999px;
            }

            .progress-fill-amber {
                height: 100%;
                background: linear-gradient(90deg, #f59e0b, #d97706);
                border-radius: 9999px;
            }

            /* --- 6. Streamlit Expander Overhauls --- */
            div[data-testid="stExpander"] {
                background: rgba(255, 255, 255, 0.88) !important;
                backdrop-filter: blur(14px) !important;
                -webkit-backdrop-filter: blur(14px) !important;
                border: 1.5px solid rgba(226, 232, 240, 0.9) !important;
                border-radius: 16px !important;
                margin-bottom: 14px !important;
                box-shadow: 0 4px 16px -4px rgba(15, 23, 42, 0.04) !important;
                overflow: hidden !important;
                transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
            }

            div[data-testid="stExpander"]:hover {
                border-color: rgba(99, 102, 241, 0.35) !important;
                box-shadow: 0 8px 24px -6px rgba(99, 102, 241, 0.12) !important;
            }

            div[data-testid="stExpander"] summary {
                padding: 14px 18px !important;
                font-weight: 800 !important;
                color: #0f172a !important;
                font-size: clamp(0.9rem, 2vw, 1.02rem) !important;
            }

            /* --- 7. Modern Button Enhancements --- */
            div[data-testid="stButton"] button[kind="primary"] {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%) !important;
                border: none !important;
                color: #ffffff !important;
                border-radius: 12px !important;
                padding: 10px 20px !important;
                font-weight: 700 !important;
                box-shadow: 0 8px 20px -4px rgba(124, 58, 237, 0.4) !important;
                transition: all 0.2s ease !important;
            }

            div[data-testid="stButton"] button[kind="primary"]:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 12px 28px -4px rgba(124, 58, 237, 0.6) !important;
            }

            .glass-divider {
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(203, 213, 225, 0.9), transparent);
                margin: 1.8rem 0 1.2rem 0;
                border: 0;
            }

            @media (max-width: 768px) {
                .history-scope { padding: 0; }
                .stat-card-glow {
                    padding: 14px;
                    border-radius: 14px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _format_date(iso_str: str) -> str:
    """Safely format ISO timestamp strings into readable dates."""
    if not iso_str:
        return "Unknown Date"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y · %I:%M %p")
    except Exception:
        return iso_str[:10] if len(iso_str) >= 10 else iso_str


def _get_score_badge_html(score: float) -> str:
    """Generate styled HTML pill depending on the overall score."""
    if score >= 80:
        cls_name = "pill-high"
        label = "High Match"
        icon = "✨"
    elif score >= 60:
        cls_name = "pill-mid"
        label = "Moderate"
        icon = "⚡"
    else:
        cls_name = "pill-low"
        label = "Needs Optimization"
        icon = "⚠️"

    return f'<span class="score-pill-pro {cls_name}">{icon} {score:.0f}/100 · {label}</span>'


def _show_backend_error(exc: Exception) -> None:
    """Render friendly backend error message."""
    if isinstance(exc, requests.ConnectionError):
        st.error("🔌 Unable to connect to the backend server. Verify the FastAPI service is running on port 8000.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        st.error(f"⚠️ Service error ({exc.response.status_code}): {exc.response.text}")
    else:
        st.error(f"⚠️ Unexpected system error: {exc}")


def _render_progress_card(label: str, score: float, max_score: float, fill_type: str = "indigo"):
    """Render a clean gradient progress bar metric tile."""
    pct = min(100.0, max(0.0, (score / max_score) * 100)) if max_score > 0 else 0
    fill_cls = f"progress-fill-{fill_type}"

    st.markdown(
        f"""
        <div class="metric-box-glass">
            <div class="metric-box-header">
                <span class="metric-box-title">{label}</span>
                <span class="metric-box-val">{score:.0f} <span style="font-size: 0.74rem; color: #64748b;">/ {max_score:.0f}</span></span>
            </div>
            <div class="progress-track-pro">
                <div class="{fill_cls}" style="width: {pct:.1f}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    """Render the responsive, modernized ATS Analysis Ledger."""
    inject_custom_css()

    st.markdown('<div class="history-scope">', unsafe_allow_html=True)

    # --- Header Section ---
    st.markdown(
        """
        <div class="history-badge-pill">⚡ Historical Records</div>
        <h1 class="history-main-title">Analysis <span>Audit Ledger</span></h1>
        <p class="history-main-desc">
            Review previous ATS evaluations, check dimension scores, and track your document optimization trajectory.
        </p>
        """,
        unsafe_allow_html=True,
    )

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.warning("🔒 Please sign in from the sidebar to access your saved resume evaluations.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # --- Data Retrieval ---
    try:
        with st.spinner("Fetching evaluation records..."):
            history: List[Dict[str, Any]] = api_client.get_history(access_token) or []
    except requests.RequestException as exc:
        _show_backend_error(exc)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    if not history:
        st.info("No audit evaluations found for this account. Run an analysis on the ATS Scorer view to populate your ledger.")
        if st.button("🚀 Launch ATS Scorer", type="primary"):
            st.session_state.current_view = "scorer"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # --- Summary KPI Metrics Bar ---
    total_evals = len(history)
    scores = [float(item.get("ats_score", 0)) for item in history]
    avg_score = sum(scores) / total_evals if total_evals > 0 else 0
    top_score = max(scores) if total_evals > 0 else 0

    m1, m2, m3 = st.columns(3, gap="medium")
    with m1:
        st.markdown(
            f"""
            <div class="stat-card-glow stat-card-indigo">
                <div class="stat-label-wrap"><span>📊</span> Total Audits</div>
                <div class="stat-value">{total_evals}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="stat-card-glow stat-card-cyan">
                <div class="stat-label-wrap"><span>📈</span> Average ATS Score</div>
                <div class="stat-value">{avg_score:.1f} <span style="font-size: 0.82rem; color: #64748b; font-weight: 600;">/ 100</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="stat-card-glow stat-card-emerald">
                <div class="stat-label-wrap"><span>🏆</span> Top Evaluation</div>
                <div class="stat-value">{top_score:.0f} <span style="font-size: 0.82rem; color: #64748b; font-weight: 600;">/ 100</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Search & Filter Controls ---
    search_col, sort_col = st.columns([2, 1], gap="medium")
    with search_col:
        search_query = st.text_input(
            "🔍 Search evaluations",
            placeholder="Search documents by filename...",
            label_visibility="collapsed",
        )
    with sort_col:
        sort_by = st.selectbox(
            "Sort order",
            options=["Newest First", "Highest Score", "Lowest Score"],
            label_visibility="collapsed",
        )

    # Apply Search Filter
    filtered_history = [
        item for item in history
        if search_query.lower() in str(item.get("filename", "")).lower()
    ]

    # Apply Sorting
    if sort_by == "Highest Score":
        filtered_history.sort(key=lambda x: float(x.get("ats_score", 0)), reverse=True)
    elif sort_by == "Lowest Score":
        filtered_history.sort(key=lambda x: float(x.get("ats_score", 0)))
    else:
        filtered_history.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)

    if not filtered_history:
        st.caption("No matching audit logs found for your search query.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown("<div class='glass-divider'></div>", unsafe_allow_html=True)

    # --- Ledger Entries ---
    for idx, entry in enumerate(filtered_history):
        filename = entry.get("filename", "Untitled Document.pdf")
        ats_score = float(entry.get("ats_score", 0))
        created_at_raw = entry.get("created_at", "")
        formatted_date = _format_date(created_at_raw)
        entry_id = entry.get("id")

        analysis = entry.get("analysis_result", {}) or {}
        component_scores = analysis.get("component_scores", {}) or {}
        jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")

        header_label = f"📄 {filename}   •   Score: {ats_score:.0f}/100   •   {formatted_date}"

        with st.expander(header_label, expanded=(idx == 0 and not search_query)):
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
                    <div>
                        <strong style="color: #0f172a; font-size: 1.1rem; font-weight: 800;">{filename}</strong>
                        <div style="color: #64748b; font-size: 0.82rem; margin-top: 2px;">🕒 Evaluated on {formatted_date}</div>
                    </div>
                    <div>{_get_score_badge_html(ats_score)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # --- Dimension Breakdown Grid ---
            col_left, col_right = st.columns(2, gap="medium")

            with col_left:
                st.markdown("<p style='font-size: 0.85rem; font-weight: 800; color: #0f172a; margin-bottom: 8px;'>📐 Structure & Layout</p>", unsafe_allow_html=True)
                _render_progress_card("Formatting & Layout", float(component_scores.get("formatting", 0)), 20.0, "indigo")
                _render_progress_card("Content & Action Impact", float(component_scores.get("content", 0)), 25.0, "indigo")
                _render_progress_card("ATS Engine Compatibility", float(component_scores.get("ats_compatibility", 0)), 15.0, "indigo")

            with col_right:
                st.markdown("<p style='font-size: 0.85rem; font-weight: 800; color: #0f172a; margin-bottom: 8px;'>🔑 Skills & Role Fit</p>", unsafe_allow_html=True)
                _render_progress_card("Keyword Density & Entities", float(component_scores.get("keywords", 0)), 25.0, "emerald")
                _render_progress_card("Skill Taxonomy Validation", float(component_scores.get("skill_validation", 0)), 15.0, "emerald")

                if jd_comparison:
                    match_pct = float(jd_comparison.get("match_percentage", 0))
                    _render_progress_card("Job Description Match", match_pct, 100.0, "amber")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            # --- Actions & Safe Removal ---
            action_col1, action_col2 = st.columns([4, 1])

            with action_col2:
                if entry_id:
                    confirm_key = f"confirm_del_{entry_id}"
                    if st.session_state.get(confirm_key):
                        st.warning("Confirm removal?")
                        c_yes, c_no = st.columns(2)
                        with c_yes:
                            if st.button("Yes", key=f"btn_yes_{entry_id}", type="primary"):
                                try:
                                    api_client.delete_history_entry(str(entry_id), access_token)
                                    st.session_state[confirm_key] = False
                                    st.toast("Record deleted.", icon="🗑️")
                                    st.rerun()
                                except requests.RequestException as exc:
                                    _show_backend_error(exc)
                        with c_no:
                            if st.button("No", key=f"btn_no_{entry_id}"):
                                st.session_state[confirm_key] = False
                                st.rerun()
                    else:
                        if st.button("🗑️ Delete", key=f"del_btn_{entry_id}", use_container_width=True):
                            st.session_state[confirm_key] = True
                            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)