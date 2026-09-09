import streamlit as st


def inject_custom_css():
    """Inject a bold, responsive multi-color design system and global canvas styling."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@600;700&display=swap');

            /* --- 1. Force Global Multi-Color Mesh Canvas on Streamlit Roots --- */
            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stHeader"] {
                background: 
                    radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.14) 0px, transparent 50%),
                    radial-gradient(at 100% 0%, rgba(14, 165, 233, 0.12) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.10) 0px, transparent 50%),
                    radial-gradient(at 0% 100%, rgba(16, 185, 129, 0.10) 0px, transparent 50%),
                    radial-gradient(at 50% 50%, rgba(139, 92, 246, 0.08) 0px, transparent 60%),
                    #f8fafc !important;
                background-attachment: fixed !important;
            }

            header[data-testid="stHeader"] {
                background: transparent !important;
            }

            /* --- 2. Typography & Responsive Geometry --- */
            .landing-scope, .landing-scope * {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
                box-sizing: border-box !important;
            }

            .landing-scope {
                width: 100%;
                max-width: 1150px;
                margin: 0 auto;
                padding: 0 4px;
            }

            .section-badge-pill {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 12px;
                border-radius: 9999px;
                background: rgba(99, 102, 241, 0.12);
                border: 1px solid rgba(99, 102, 241, 0.3);
                color: #4f46e5;
                font-size: 0.76rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: 6px;
            }

            .section-heading {
                color: #0f172a;
                font-size: clamp(1.25rem, 3vw, 1.6rem);
                font-weight: 800;
                letter-spacing: -0.02em;
                margin: 0 0 4px 0;
            }

            .section-subtext {
                color: #475569;
                font-size: clamp(0.85rem, 1.8vw, 0.95rem);
                margin: 0 0 18px 0;
            }

            /* --- 3. High-Contrast Frosted Glass Feature Cards --- */
            .pro-card-modern {
                background: rgba(255, 255, 255, 0.88) !important;
                backdrop-filter: blur(14px) !important;
                -webkit-backdrop-filter: blur(14px) !important;
                border-radius: 18px;
                padding: clamp(18px, 2.5vw, 24px);
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                margin-bottom: 14px;
                position: relative;
                transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .pro-card-modern:hover {
                transform: translateY(-4px);
            }

            /* Card Top Vibrant Accent Glows */
            .accent-indigo {
                border: 1.5px solid rgba(99, 102, 241, 0.4) !important;
                box-shadow: 0 8px 24px -6px rgba(99, 102, 241, 0.16) !important;
            }
            .accent-indigo:hover {
                box-shadow: 0 16px 32px -6px rgba(99, 102, 241, 0.28) !important;
                border-color: #6366f1 !important;
            }

            .accent-amber {
                border: 1.5px solid rgba(245, 158, 11, 0.4) !important;
                box-shadow: 0 8px 24px -6px rgba(245, 158, 11, 0.16) !important;
            }
            .accent-amber:hover {
                box-shadow: 0 16px 32px -6px rgba(245, 158, 11, 0.28) !important;
                border-color: #f59e0b !important;
            }

            .accent-emerald {
                border: 1.5px solid rgba(16, 185, 129, 0.4) !important;
                box-shadow: 0 8px 24px -6px rgba(16, 185, 129, 0.16) !important;
            }
            .accent-emerald:hover {
                box-shadow: 0 16px 32px -6px rgba(16, 185, 129, 0.28) !important;
                border-color: #10b981 !important;
            }

            .accent-neutral {
                border: 1.5px solid rgba(203, 213, 225, 0.9) !important;
                box-shadow: 0 8px 24px -6px rgba(15, 23, 42, 0.06) !important;
            }
            .accent-neutral:hover {
                box-shadow: 0 16px 32px -6px rgba(15, 23, 42, 0.12) !important;
                border-color: #94a3b8 !important;
            }

            /* --- 4. Micro Badges & Icons --- */
            .card-icon-pill {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 44px;
                height: 44px;
                border-radius: 12px;
                font-size: 1.35rem;
                margin-bottom: 14px;
            }
            .icon-bg-indigo  { background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); border: 1px solid #c7d2fe; color: #4338ca; }
            .icon-bg-amber   { background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 1px solid #fde68a; color: #b45309; }
            .icon-bg-emerald { background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border: 1px solid #a7f3d0; color: #047857; }

            .step-number-badge {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 36px;
                height: 36px;
                border-radius: 10px;
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                color: #ffffff;
                font-weight: 800;
                font-size: 0.95rem;
                margin-bottom: 12px;
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
            }

            .card-title {
                font-size: clamp(1.05rem, 2vw, 1.18rem);
                font-weight: 800;
                color: #0f172a;
                margin: 0 0 6px 0;
            }

            .card-body-text {
                color: #475569;
                font-size: clamp(0.85rem, 1.8vw, 0.92rem);
                line-height: 1.55;
                margin: 0;
            }

            /* Sub-Pills */
            .info-tag {
                margin-top: 14px;
                padding: 6px 12px;
                border-radius: 8px;
                font-size: 0.78rem;
                font-weight: 700;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }

            .tag-amber {
                background: #fffbeb;
                border: 1px solid #fde68a;
                color: #92400e;
            }

            .tag-emerald {
                background: #ecfdf5;
                border: 1px solid #a7f3d0;
                color: #065f46;
            }

            .score-breakdown-list {
                margin-top: 10px;
                padding-left: 0;
                list-style: none;
                font-size: 0.84rem;
                color: #334155;
                line-height: 1.65;
            }

            .score-breakdown-list li {
                display: flex;
                justify-content: space-between;
                border-bottom: 1px dashed #e2e8f0;
                padding: 4px 0;
            }

            /* --- 5. Mobile-Optimized CTA Launch Button --- */
            div[data-testid="stButton"] button[kind="primary"] {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%) !important;
                border: none !important;
                color: #ffffff !important;
                border-radius: 12px !important;
                padding: 12px 28px !important;
                font-size: clamp(0.95rem, 2.2vw, 1.1rem) !important;
                font-weight: 800 !important;
                box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.4) !important;
                transition: all 0.25s ease !important;
                min-height: 52px !important;
            }

            div[data-testid="stButton"] button[kind="primary"]:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 16px 32px -5px rgba(124, 58, 237, 0.6) !important;
            }

            @media (max-width: 768px) {
                .landing-scope {
                    padding: 0;
                }
                .pro-card-modern {
                    padding: 16px;
                    margin-bottom: 12px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    """Render the responsive, professional ResumeIQ Landing view."""
    inject_custom_css()

    # --- 1. Responsive Hero Canvas (iframe embed) ---
    hero_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            body {
                background: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 6px 2px;
                overflow: hidden;
            }
            .landing-hero {
                position: relative;
                width: 100%;
                max-width: 1100px;
                background:
                    radial-gradient(ellipse 70% 60% at 15% 0%, rgba(99, 102, 241, 0.45) 0%, transparent 70%),
                    radial-gradient(ellipse 65% 55% at 85% 10%, rgba(14, 165, 233, 0.35) 0%, transparent 70%),
                    radial-gradient(ellipse 55% 65% at 50% 100%, rgba(236, 72, 153, 0.25) 0%, transparent 80%),
                    linear-gradient(180deg, #090d16 0%, #0f172a 100%);
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 22px;
                padding: clamp(1.8rem, 4vw, 2.8rem) clamp(1.2rem, 3.5vw, 2.4rem);
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                box-shadow: 0 20px 45px -10px rgba(15, 23, 42, 0.5), 0 0 40px -10px rgba(99, 102, 241, 0.3);
                overflow: hidden;
            }
            .hero-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 16px;
                background: rgba(255, 255, 255, 0.09);
                border: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 9999px;
                color: #c7d2fe;
                font-size: clamp(0.72rem, 1.5vw, 0.8rem);
                font-weight: 800;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin-bottom: 1rem;
                backdrop-filter: blur(10px);
            }
            .hero-title {
                font-size: clamp(1.75rem, 4.8vw, 2.9rem);
                font-weight: 900;
                color: #ffffff;
                line-height: 1.18;
                letter-spacing: -0.03em;
                margin-bottom: 0.75rem;
            }
            .hero-title span {
                background: linear-gradient(135deg, #38bdf8 0%, #818cf8 45%, #ec4899 100%);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .typewriter-container {
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 28px;
                margin-bottom: 0.85rem;
                font-size: clamp(0.9rem, 2.2vw, 1.18rem);
                font-weight: 700;
                color: #f1f5f9;
                text-align: center;
            }
            .cursor {
                display: inline-block;
                color: #38bdf8;
                font-weight: 800;
                margin-left: 4px;
                animation: blink 0.75s infinite;
            }
            .hero-subtitle {
                color: #94a3b8;
                font-size: clamp(0.85rem, 1.8vw, 0.98rem);
                line-height: 1.6;
                max-width: 680px;
                margin: 0 auto;
            }
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
        </style>
    </head>
    <body>
        <div class="landing-hero">
            <div class="hero-badge">⚡ Next-Gen ATS Resume Intelligence</div>
            <h1 class="hero-title">Optimize Your Resume <span>For ATS Algorithms</span></h1>
            <div class="typewriter-container">
                <span id="type-text"></span><span class="cursor">|</span>
            </div>
            <p class="hero-subtitle">
                Benchmark keyword extraction, semantic relevance, structural hierarchy, and authentic project validation before submitting your application.
            </p>
        </div>

        <script>
            const phrases = [
                "Eliminate hidden formatting and parsing blockers",
                "Validate authentic project evidence behind your skills",
                "Benchmark entity coverage against target job postings",
                "Elevate your interview callback rate with actionable fixes"
            ];

            let pIdx = 0;
            let cIdx = 0;
            let deleting = false;
            const target = document.getElementById("type-text");

            function typeWriter() {
                const current = phrases[pIdx];
                if (deleting) {
                    target.textContent = current.substring(0, cIdx - 1);
                    cIdx--;
                } else {
                    target.textContent = current.substring(0, cIdx + 1);
                    cIdx++;
                }

                let speed = deleting ? 18 : 40;

                if (!deleting && cIdx === current.length) {
                    speed = 2200;
                    deleting = true;
                } else if (deleting && cIdx === 0) {
                    deleting = false;
                    pIdx = (pIdx + 1) % phrases.length;
                    speed = 250;
                }

                setTimeout(typeWriter, speed);
            }
            typeWriter();
        </script>
    </body>
    </html>
    """

    st.iframe(hero_html, height=325)

    # --- 2. Primary Launch Action ---
    _, c_btn, _ = st.columns([1, 2, 1])
    with c_btn:
        if st.button("🚀 Launch Resume Analyzer", use_container_width=True, type="primary"):
            st.session_state.current_view = "scorer"
            st.rerun()

    # --- 3. Core Evaluation Vector Breakdown ---
    st.markdown(
        """
        <div class="landing-scope" style="margin-top: 1.5rem;">
            <div class="section-badge-pill">Diagnostic Architecture</div>
            <div class="section-heading">Core Evaluation Engines</div>
            <p class="section-subtext">Comprehensive multi-vector diagnostics designed to mirror tier-1 ATS logic.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns([1, 1, 1], gap="medium")

    with f1:
        st.markdown(
            """
            <div class="landing-scope">
                <div class="pro-card-modern accent-indigo">
                    <div>
                        <div class="card-icon-pill icon-bg-indigo">📊</div>
                        <div class="card-title">Multi-Vector Scoring</div>
                        <p class="card-body-text">5-dimensional heuristic analysis evaluating core ATS parameters:</p>
                        <ul class="score-breakdown-list">
                            <li><span>Formatting & Layout</span><strong>20%</strong></li>
                            <li><span>Keyword Alignment</span><strong>25%</strong></li>
                            <li><span>Content Quality</span><strong>25%</strong></li>
                            <li><span>Skill Evidence</span><strong>15%</strong></li>
                            <li><span>Parser Compatibility</span><strong>15%</strong></li>
                        </ul>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with f2:
        st.markdown(
            """
            <div class="landing-scope">
                <div class="pro-card-modern accent-amber">
                    <div>
                        <div class="card-icon-pill icon-bg-amber">🔍</div>
                        <div class="card-title">Skill Evidence Matrix</div>
                        <p class="card-body-text">
                            Cross-references listed technical skills against bullet-point descriptions to detect unvalidated or empty claims.
                        </p>
                    </div>
                    <div>
                        <div class="info-tag tag-amber">
                            <span>💡</span> Contextual verification proof
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with f3:
        st.markdown(
            """
            <div class="landing-scope">
                <div class="pro-card-modern accent-emerald">
                    <div>
                        <div class="card-icon-pill icon-bg-emerald">🔒</div>
                        <div class="card-title">Enterprise Privacy</div>
                        <p class="card-body-text">
                            Files are processed in isolated runtime sessions with strict encryption standards and zero permanent data exposure.
                        </p>
                    </div>
                    <div>
                        <div class="info-tag tag-emerald">
                            <span>🛡️</span> Ephemeral & sandboxed
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- 4. Optimization Workflow ---
    st.markdown(
        """
        <div class="landing-scope" style="margin-top: 1.5rem;">
            <div class="section-badge-pill">Execution Pipeline</div>
            <div class="section-heading">3-Step Optimization Workflow</div>
            <p class="section-subtext">Streamlined diagnostic pipeline from upload to downloadable report.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    s1, s2, s3 = st.columns([1, 1, 1], gap="medium")

    with s1:
        st.markdown(
            """
            <div class="landing-scope">
                <div class="pro-card-modern accent-neutral">
                    <div>
                        <div class="step-number-badge">1</div>
                        <div class="card-title">Document Ingestion</div>
                        <p class="card-body-text">Upload your PDF or DOCX file along with an optional target job description.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s2:
        st.markdown(
            """
            <div class="landing-scope">
                <div class="pro-card-modern accent-neutral">
                    <div>
                        <div class="step-number-badge">2</div>
                        <div class="card-title">NLP & Taxonomy Scan</div>
                        <p class="card-body-text">Automated parsers perform entity matching, semantic similarity, and layout checks.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s3:
        st.markdown(
            """
            <div class="landing-scope">
                <div class="pro-card-modern accent-neutral">
                    <div>
                        <div class="step-number-badge">3</div>
                        <div class="card-title">Audit & Remediation</div>
                        <p class="card-body-text">Review granular feedback checklists and export structured PDF audit reports.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )