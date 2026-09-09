from typing import Optional
import requests
import streamlit as st

from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard


def inject_custom_css():
    """Inject modern, responsive styling with highlighted input containers and luminous button typography."""
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

            /* --- 2. Typography & Layout Containers --- */
            .scorer-scope, .scorer-scope * {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
                box-sizing: border-box !important;
            }

            .scorer-scope {
                width: 100%;
                max-width: 1180px;
                margin: 0 auto;
                padding: 0 4px;
            }

            .scorer-badge-pill {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 5px 14px;
                border-radius: 9999px;
                background: rgba(99, 102, 241, 0.14);
                border: 1.5px solid rgba(99, 102, 241, 0.35);
                color: #4338ca;
                font-size: 0.76rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: 8px;
            }

            .scorer-main-title {
                color: #0f172a;
                font-size: clamp(1.6rem, 4vw, 2.5rem);
                font-weight: 900;
                letter-spacing: -0.03em;
                line-height: 1.2;
                margin: 0 0 6px 0;
            }

            .scorer-main-title span {
                background: linear-gradient(135deg, #4f46e5 0%, #0ea5e9 50%, #ec4899 100%);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .scorer-main-desc {
                color: #475569;
                font-size: clamp(0.88rem, 1.8vw, 1rem);
                line-height: 1.55;
                margin: 0 0 24px 0;
            }

            /* --- 3. Highlighted Input Card Containers --- */
            .glass-card-upload {
                background: rgba(255, 255, 255, 0.92) !important;
                backdrop-filter: blur(16px) !important;
                -webkit-backdrop-filter: blur(16px) !important;
                border-radius: 18px;
                padding: clamp(18px, 2.5vw, 24px);
                margin-bottom: 12px;
                box-shadow: 0 10px 30px -8px rgba(15, 23, 42, 0.08);
                position: relative;
                overflow: hidden;
                border: 1.5px solid rgba(226, 232, 240, 0.95);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .card-accent-indigo {
                border-top: 4px solid #6366f1 !important;
                box-shadow: 0 8px 24px -6px rgba(99, 102, 241, 0.15) !important;
            }
            .card-accent-indigo:hover {
                border-color: #6366f1 !important;
                box-shadow: 0 16px 36px -6px rgba(99, 102, 241, 0.28) !important;
                transform: translateY(-2px);
            }

            .card-accent-cyan {
                border-top: 4px solid #0ea5e9 !important;
                box-shadow: 0 8px 24px -6px rgba(14, 165, 233, 0.15) !important;
            }
            .card-accent-cyan:hover {
                border-color: #0ea5e9 !important;
                box-shadow: 0 16px 36px -6px rgba(14, 165, 233, 0.28) !important;
                transform: translateY(-2px);
            }

            .card-header-flex {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 14px;
                padding-bottom: 8px;
                border-bottom: 1px solid rgba(226, 232, 240, 0.8);
            }

            .step-icon-badge {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                border-radius: 12px;
                font-size: 1.3rem;
            }
            .step-icon-indigo { background: #eef2ff; border: 1.5px solid #c7d2fe; color: #4338ca; }
            .step-icon-cyan   { background: #f0f9ff; border: 1.5px solid #bae6fd; color: #0369a1; }

            .card-step-title {
                font-size: clamp(1.05rem, 2vw, 1.2rem);
                font-weight: 800;
                color: #0f172a;
                margin: 0 0 2px 0;
            }

            .card-step-desc {
                font-size: 0.84rem;
                color: #64748b;
                margin: 0;
            }

            /* --- 4. Form & Input Box Element Highlights --- */
            div[data-testid="stFileUploader"] {
                background: #ffffff !important;
                border: 2px dashed #cbd5e1 !important;
                border-radius: 14px !important;
                padding: 10px !important;
                transition: all 0.25s ease !important;
            }

            div[data-testid="stFileUploader"]:hover {
                border-color: #6366f1 !important;
                background: #f8faff !important;
                box-shadow: 0 4px 16px rgba(99, 102, 241, 0.12) !important;
            }

            div[data-testid="stTextArea"] textarea {
                background: #ffffff !important;
                border: 1.5px solid #cbd5e1 !important;
                border-radius: 12px !important;
                color: #0f172a !important;
                font-size: 0.9rem !important;
                padding: 12px !important;
                transition: all 0.25s ease !important;
            }

            div[data-testid="stTextArea"] textarea:focus {
                border-color: #0ea5e9 !important;
                box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.25) !important;
            }

            div[data-testid="stRadio"] > div {
                gap: 16px !important;
                background: #f1f5f9 !important;
                padding: 6px 14px !important;
                border-radius: 10px !important;
                border: 1px solid #e2e8f0 !important;
                width: fit-content !important;
                margin-bottom: 8px !important;
            }

            /* --- 5. High-Impact CTA Button with Highlighted Typography --- */
            div[data-testid="stButton"] button[kind="primary"] {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%) !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                border-radius: 14px !important;
                padding: 14px 28px !important;
                box-shadow: 0 10px 25px -4px rgba(124, 58, 237, 0.5), 0 0 15px rgba(236, 72, 153, 0.3) !important;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
                min-height: 54px !important;
            }

            /* Bold Luminous Button Typography */
            div[data-testid="stButton"] button[kind="primary"] p,
            div[data-testid="stButton"] button[kind="primary"] span {
                color: #ffffff !important;
                font-weight: 900 !important;
                font-size: clamp(0.98rem, 2.2vw, 1.15rem) !important;
                letter-spacing: 0.02em !important;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.35) !important;
            }

            div[data-testid="stButton"] button[kind="primary"]:hover {
                transform: translateY(-2px) scale(1.01) !important;
                box-shadow: 0 16px 36px -4px rgba(124, 58, 237, 0.7), 0 0 25px rgba(236, 72, 153, 0.5) !important;
            }

            /* Disabled Button State */
            div[data-testid="stButton"] button:disabled {
                background: #e2e8f0 !important;
                border: 1.5px solid #cbd5e1 !important;
                box-shadow: none !important;
                transform: none !important;
                cursor: not-allowed !important;
            }

            div[data-testid="stButton"] button:disabled p,
            div[data-testid="stButton"] button:disabled span {
                color: #94a3b8 !important;
                text-shadow: none !important;
                font-weight: 700 !important;
            }

            .glass-divider {
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(203, 213, 225, 0.9), transparent);
                margin: 2rem 0;
                border: 0;
            }

            @media (max-width: 768px) {
                .scorer-scope {
                    padding: 0;
                }
                .glass-card-upload {
                    padding: 16px;
                    border-radius: 14px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _read_jd(jd_file, jd_text: str) -> str:
    """Safely extracts JD content from text area or uploaded file."""
    if jd_text:
        return jd_text.strip()
    if jd_file is None:
        return ""
    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode("utf-8", errors="ignore")
    st.warning("⚠️ Job description files must be `.txt`. Please paste text instead.")
    return ""


def _show_backend_error(exc: Exception) -> None:
    """Render structured backend error diagnostics."""
    if isinstance(exc, requests.ConnectionError):
        st.error("🔌 Could not connect to the backend server. Verify the FastAPI service is running on port 8000.")
    elif isinstance(exc, requests.Timeout):
        st.error("⏱️ The backend analysis request timed out. Please try again.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"⚠️ Backend returned error ({exc.response.status_code}): {detail}")
    else:
        st.error(f"⚠️ Analysis error: {exc}")


def render() -> None:
    """Render the responsive, modernized ATS Resume Scorer."""
    inject_custom_css()

    st.markdown('<div class="scorer-scope">', unsafe_allow_html=True)

    # --- Header Section ---
    st.markdown(
        """
        <div class="scorer-badge-pill">⚡ Neural Diagnostic Engine</div>
        <h1 class="scorer-main-title">Resume <span>ATS Optimizer</span></h1>
        <p class="scorer-main-desc">
            Benchmark layout integrity, extract semantic keyword coverage, and surface actionable fixes to maximize interview callbacks.
        </p>
        """,
        unsafe_allow_html=True,
    )

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.warning("🔒 Please sign in from the left sidebar to analyze and save document evaluations.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # --- Upload Matrix ---
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div class="glass-card-upload card-accent-indigo">
                <div class="card-header-flex">
                    <div class="step-icon-badge step-icon-indigo">📄</div>
                    <div>
                        <div class="card-step-title">1. Target Resume</div>
                        <p class="card-step-desc">Accepts PDF, DOCX, or DOC formats (Max 10 MB)</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        resume_file = st.file_uploader(
            "Upload candidate resume",
            type=["pdf", "doc", "docx"],
            label_visibility="collapsed",
            key="resume_uploader_main",
        )
        if resume_file:
            st.success(f"✓ Loaded: **{resume_file.name}** ({resume_file.size / 1024:.1f} KB)")

    with col_right:
        st.markdown(
            """
            <div class="glass-card-upload card-accent-cyan">
                <div class="card-header-flex">
                    <div class="step-icon-badge step-icon-cyan">📋</div>
                    <div>
                        <div class="card-step-title">2. Job Description (Optional)</div>
                        <p class="card-step-desc">Add target role for contextual keyword gap alignment</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        jd_choice = st.radio("Input format", ["Paste Text", "Upload .txt"], horizontal=True, label_visibility="collapsed")
        jd_file, jd_text = None, ""
        if jd_choice == "Upload .txt":
            jd_file = st.file_uploader("Upload JD", type=["txt"], key="jd_file_up", label_visibility="collapsed")
            if jd_file:
                st.success(f"✓ Loaded JD: **{jd_file.name}**")
        else:
            jd_text = st.text_area(
                "Paste JD content",
                height=130,
                placeholder="Paste requirements, core responsibilities, and qualifications here...",
                label_visibility="collapsed",
            )
            if jd_text:
                st.caption(f"✓ {len(jd_text):,} characters entered")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # --- Primary Trigger CTA ---
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        analyze_clicked = st.button(
            "🚀 Run Comprehensive ATS Analysis",
            use_container_width=True,
            type="primary",
            disabled=(resume_file is None),
        )

    if analyze_clicked:
        st.session_state.pop("dashboard_pdf_bytes", None)
        st.session_state.pop("scorer_analysis", None)
        jd_content = _read_jd(jd_file, jd_text)
        try:
            with st.spinner("AI parsing in progress (evaluating structure, semantics, and keywords)..."):
                analysis = api_client.analyze_resume(
                    resume_file=resume_file,
                    access_token=access_token,
                    job_description=jd_content,
                )
                st.session_state["scorer_analysis"] = analysis
                st.toast("Evaluation complete!", icon="🎯")
        except requests.RequestException as exc:
            _show_backend_error(exc)

    # --- Results Dashboard Section ---
    if st.session_state.get("scorer_analysis"):
        st.markdown("<div class='glass-divider'></div>", unsafe_allow_html=True)
        display_results_dashboard(st.session_state["scorer_analysis"])

    st.markdown('</div>', unsafe_allow_html=True)