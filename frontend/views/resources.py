import streamlit as st


def inject_custom_css():
    """Inject responsive modern styling, glowing segmented tab capsule, and frosted glass cards."""
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
            .resources-scope, .resources-scope * {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
                box-sizing: border-box !important;
            }

            .resources-scope {
                width: 100%;
                max-width: 1180px;
                margin: 0 auto;
                padding: 0 4px;
            }

            .hero-badge-pill {
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

            .main-title {
                color: #0f172a;
                font-size: clamp(1.6rem, 4vw, 2.5rem);
                font-weight: 900;
                letter-spacing: -0.03em;
                line-height: 1.2;
                margin: 0 0 6px 0;
            }

            .main-title span {
                background: linear-gradient(135deg, #4f46e5 0%, #0ea5e9 50%, #ec4899 100%);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .main-desc {
                color: #475569;
                font-size: clamp(0.88rem, 1.8vw, 1rem);
                line-height: 1.55;
                margin: 0 0 24px 0;
            }

            .section-heading {
                color: #0f172a;
                font-size: clamp(1.15rem, 2.5vw, 1.38rem);
                font-weight: 800;
                letter-spacing: -0.02em;
                margin: 28px 0 4px 0;
            }

            .section-caption {
                color: #64748b;
                font-size: clamp(0.82rem, 1.8vw, 0.9rem);
                margin: 0 0 16px 0;
            }

            /* --- 3. Best Practices Matrix Cards --- */
            .glass-pro-card {
                background: rgba(255, 255, 255, 0.88) !important;
                backdrop-filter: blur(14px) !important;
                -webkit-backdrop-filter: blur(14px) !important;
                border-radius: 18px;
                padding: clamp(16px, 2.5vw, 22px);
                height: 100%;
                display: flex;
                flex-direction: column;
                margin-bottom: 14px;
                transition: transform 0.25s ease, box-shadow 0.25s ease;
            }

            .glass-pro-card:hover { transform: translateY(-3px); }

            .card-do {
                border: 1.5px solid rgba(16, 185, 129, 0.35) !important;
                border-top: 4px solid #10b981 !important;
                box-shadow: 0 8px 24px -6px rgba(16, 185, 129, 0.12);
            }
            .card-do:hover {
                border-color: #10b981 !important;
                box-shadow: 0 14px 30px -6px rgba(16, 185, 129, 0.22);
            }

            .card-dont {
                border: 1.5px solid rgba(239, 68, 68, 0.35) !important;
                border-top: 4px solid #ef4444 !important;
                box-shadow: 0 8px 24px -6px rgba(239, 68, 68, 0.12);
            }
            .card-dont:hover {
                border-color: #ef4444 !important;
                box-shadow: 0 14px 30px -6px rgba(239, 68, 68, 0.22);
            }

            .card-header-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 14px;
                padding-bottom: 10px;
                border-bottom: 1px solid rgba(226, 232, 240, 0.8);
            }

            .card-heading {
                font-size: clamp(1rem, 2vw, 1.12rem);
                font-weight: 800;
                margin: 0;
            }
            .heading-do { color: #065f46; }
            .heading-dont { color: #991b1b; }

            .tag-status {
                font-size: 0.72rem;
                font-weight: 800;
                padding: 4px 10px;
                border-radius: 9999px;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }
            .tag-do { background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
            .tag-dont { background-color: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

            .list-item {
                display: flex;
                align-items: flex-start;
                gap: 10px;
                margin-bottom: 12px;
            }

            .bullet-check { color: #059669; font-weight: 800; font-size: 1.05rem; line-height: 1.4; flex-shrink: 0; }
            .bullet-cross { color: #dc2626; font-weight: 800; font-size: 1.05rem; line-height: 1.4; flex-shrink: 0; }

            .item-text {
                font-size: clamp(0.84rem, 1.8vw, 0.92rem);
                line-height: 1.55;
                color: #334155;
                margin: 0;
            }
            .item-text strong { color: #0f172a; font-weight: 700; }

            /* --- 4. CUSTOM HIGH-END SEGMENTED PILL TAB BAR --- */
            
            /* Remove all native tab container lines and borders */
            div[data-testid="stTabs"] {
                margin-top: 10px !important;
                margin-bottom: 1.5rem !important;
            }

            div[data-baseweb="tab-border"],
            div[data-baseweb="tab-highlight"],
            div[data-testid="stTabs"] hr {
                display: none !important;
                border: none !important;
                height: 0 !important;
            }

            /* Floating Capsule Container for Tab Buttons */
            div[data-baseweb="tab-list"],
            div[data-testid="stTabs"] > div:first-child {
                background: rgba(255, 255, 255, 0.85) !important;
                backdrop-filter: blur(16px) !important;
                -webkit-backdrop-filter: blur(16px) !important;
                border: 1.5px solid rgba(226, 232, 240, 0.95) !important;
                border-radius: 14px !important;
                padding: 6px !important;
                gap: 6px !important;
                display: flex !important;
                flex-wrap: wrap !important;
                box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.06), 0 0 1px rgba(15, 23, 42, 0.1) !important;
            }

            /* Inactive Tab Button */
            button[data-testid="stTab"],
            button[data-baseweb="tab"] {
                background: transparent !important;
                border: 1px solid transparent !important;
                border-radius: 10px !important;
                color: #475569 !important;
                font-weight: 700 !important;
                font-size: clamp(0.82rem, 1.8vw, 0.92rem) !important;
                padding: 8px 16px !important;
                height: auto !important;
                margin: 0 !important;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
                display: inline-flex !important;
                align-items: center !important;
                gap: 6px !important;
            }

            /* Inactive Tab Hover */
            button[data-testid="stTab"]:hover,
            button[data-baseweb="tab"]:hover {
                background: rgba(99, 102, 241, 0.08) !important;
                color: #4f46e5 !important;
                border-color: rgba(99, 102, 241, 0.15) !important;
                transform: translateY(-1px) !important;
            }

            /* ACTIVE TAB: High-Contrast Pill with Multi-Color Indigo Glow */
            button[data-testid="stTab"][aria-selected="true"],
            button[data-baseweb="tab"][aria-selected="true"] {
                background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #7c3aed 100%) !important;
                color: #ffffff !important;
                border-radius: 10px !important;
                border: 1px solid rgba(255, 255, 255, 0.25) !important;
                box-shadow: 0 6px 20px -4px rgba(79, 70, 229, 0.45) !important;
                transform: translateY(-1px) !important;
            }

            button[data-testid="stTab"][aria-selected="true"] p,
            button[data-baseweb="tab"][aria-selected="true"] p,
            button[data-testid="stTab"][aria-selected="true"] div,
            button[data-testid="stTab"][aria-selected="true"] span {
                color: #ffffff !important;
                font-weight: 800 !important;
            }

            /* --- 5. Categorized Keyword Container --- */
            .category-card {
                background: rgba(255, 255, 255, 0.9) !important;
                backdrop-filter: blur(14px) !important;
                -webkit-backdrop-filter: blur(14px) !important;
                border: 1px solid rgba(226, 232, 240, 0.9) !important;
                border-radius: 16px;
                padding: clamp(16px, 2.5vw, 22px);
                margin-top: 14px;
                box-shadow: 0 6px 20px -6px rgba(15, 23, 42, 0.05);
            }

            .group-heading {
                font-size: 0.82rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 6px;
            }

            .chip-container {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 14px;
            }

            .kw-chip {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 12px;
                border-radius: 8px;
                font-size: clamp(0.78rem, 1.6vw, 0.86rem);
                font-weight: 700;
                transition: all 0.2s ease;
                white-space: nowrap;
                cursor: default;
            }
            .kw-chip:hover { transform: translateY(-2px); }

            .chip-tech { background: #f0f9ff; border: 1.5px solid #bae6fd; color: #0369a1; }
            .chip-tech:hover { background: #e0f2fe; border-color: #0284c7; color: #075985; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.2); }

            .chip-biz { background: #f0fdf4; border: 1.5px solid #bbf7d0; color: #15803d; }
            .chip-biz:hover { background: #dcfce7; border-color: #16a34a; color: #166534; box-shadow: 0 4px 12px rgba(22, 163, 74, 0.2); }

            .chip-pm { background: #fff7ed; border: 1.5px solid #fed7aa; color: #c2410c; }
            .chip-pm:hover { background: #ffedd5; border-color: #ea580c; color: #9a3412; box-shadow: 0 4px 12px rgba(234, 88, 12, 0.2); }

            .chip-ux { background: #fdf4ff; border: 1.5px solid #f5d0fe; color: #a21caf; }
            .chip-ux:hover { background: #fae8ff; border-color: #c026d3; color: #86198f; box-shadow: 0 4px 12px rgba(192, 38, 211, 0.2); }

            /* --- 6. Template Cards --- */
            .template-box-glass {
                background: rgba(255, 255, 255, 0.88) !important;
                backdrop-filter: blur(14px) !important;
                border: 1.5px solid rgba(226, 232, 240, 0.9);
                border-radius: 16px;
                padding: clamp(16px, 2.5vw, 20px);
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
                margin-bottom: 10px;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
            }

            .template-box-glass:hover {
                transform: translateY(-3px);
                border-color: rgba(99, 102, 241, 0.4);
                box-shadow: 0 12px 28px -6px rgba(99, 102, 241, 0.15);
            }

            .template-title {
                font-size: clamp(0.96rem, 2vw, 1.08rem);
                font-weight: 800;
                color: #0f172a;
                margin: 0 0 6px 0;
            }

            .template-subtitle {
                font-size: clamp(0.8rem, 1.6vw, 0.86rem);
                color: #64748b;
                margin: 0 0 12px 0;
                line-height: 1.45;
            }

            div[data-testid="stButton"] button {
                width: 100% !important;
                min-height: 44px !important;
                border-radius: 10px !important;
                font-size: clamp(0.82rem, 1.6vw, 0.9rem) !important;
                font-weight: 700 !important;
                border: 1.5px solid #cbd5e1 !important;
                background: #ffffff !important;
                color: #0f172a !important;
                transition: all 0.2s ease !important;
            }

            div[data-testid="stButton"] button:hover {
                border-color: #4f46e5 !important;
                color: #4f46e5 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 18px -4px rgba(79, 70, 229, 0.15) !important;
            }

            .glass-divider {
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(203, 213, 225, 0.9), transparent);
                margin: 2rem 0 1.2rem 0;
                border: 0;
            }

            @media (max-width: 768px) {
                .resources-scope { padding: 0; }
                div[data-baseweb="tab-list"] {
                    padding: 4px !important;
                    gap: 4px !important;
                }
                button[data-testid="stTab"] {
                    padding: 6px 10px !important;
                    font-size: 0.78rem !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render():
    """Render the responsive, modernized ATS Resources view."""
    inject_custom_css()

    st.markdown('<div class="resources-scope">', unsafe_allow_html=True)

    # --- Header Section ---
    st.markdown(
        """
        <div class="hero-badge-pill">⚡ Optimization Guide</div>
        <h1 class="main-title">ATS Guidelines & <span>Best Practices</span></h1>
        <p class="main-desc">
            Actionable formatting standards and entity benchmarks engineered for tier-1 applicant tracking systems (Workday, Greenhouse, Lever, Taleo).
        </p>
        """,
        unsafe_allow_html=True,
    )

    # --- Section: Best Practices ---
    st.markdown(
        """
        <div class="section-heading">Standard ATS Compliance Rules</div>
        <p class="section-caption">Core structural practices to ensure complete and accurate data extraction.</p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown(
            """
            <div class="glass-pro-card card-do">
                <div class="card-header-row">
                    <span class="card-heading heading-do">Recommended Standards</span>
                    <span class="tag-status tag-do">Compliant</span>
                </div>
                <div class="list-item">
                    <span class="bullet-check">✓</span>
                    <p class="item-text"><strong>Direct Keyword Alignment:</strong> Mirror specific core competencies and technical tools listed in the target job spec.</p>
                </div>
                <div class="list-item">
                    <span class="bullet-check">✓</span>
                    <p class="item-text"><strong>Quantified Results:</strong> Structure bullets with <em>Action Verb + Context + Quantifiable Metric (%)</em>.</p>
                </div>
                <div class="list-item">
                    <span class="bullet-check">✓</span>
                    <p class="item-text"><strong>Standard Headings:</strong> Use universal labels (<em>Work Experience</em>, <em>Education</em>, <em>Skills</em>) to ensure accurate indexing.</p>
                </div>
                <div class="list-item">
                    <span class="bullet-check">✓</span>
                    <p class="item-text"><strong>Single-Column Layout:</strong> Maintain a vertical top-to-bottom hierarchy to avoid line merging errors.</p>
                </div>
                <div class="list-item">
                    <span class="bullet-check">✓</span>
                    <p class="item-text"><strong>Selectable Text PDFs:</strong> Export clean vector PDFs or <code>.docx</code> files without image-flattened text.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="glass-pro-card card-dont">
                <div class="card-header-row">
                    <span class="card-heading heading-dont">Practices to Avoid</span>
                    <span class="tag-status tag-dont">High Risk</span>
                </div>
                <div class="list-item">
                    <span class="bullet-cross">✕</span>
                    <p class="item-text"><strong>Multi-Column Sidebars:</strong> Text parsers read horizontally across columns, corrupting experience timelines.</p>
                </div>
                <div class="list-item">
                    <span class="bullet-cross">✕</span>
                    <p class="item-text"><strong>Header / Footer Metadata:</strong> Essential phone numbers and email links placed in margins are frequently omitted.</p>
                </div>
                <div class="list-item">
                    <span class="bullet-cross">✕</span>
                    <p class="item-text"><strong>Graphical Skill Ratings:</strong> Rating icons, progress circles, and skill meters are completely unreadable by parsers.</p>
                </div>
                <div class="list-item">
                    <span class="bullet-cross">✕</span>
                    <p class="item-text"><strong>Keyword Flooding:</strong> Hidden white text or unorganized skill dumps trigger anti-spam penalty filters.</p>
                </div>
                <div class="list-item">
                    <span class="bullet-cross">✕</span>
                    <p class="item-text"><strong>Irregular Tables:</strong> Complex table structures often break extraction ordering and misplace achievements.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Section: High-Impact Modern Tabs ---
    st.markdown(
        """
        <div class="section-heading">Industry Keyword Taxonomy</div>
        <p class="section-caption">High-frequency semantic entities indexed by modern ATS search filters.</p>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["💻 Engineering & Cloud", "📊 Business & Strategy", "🚀 Product & Operations", "🎨 Design & UX"]
    )

    with tab1:
        st.markdown(
            """
            <div class="category-card" style="border-top: 3.5px solid #0284c7 !important;">
                <div class="group-heading" style="color: #0369a1;">⚡ Core Languages & Frameworks</div>
                <div class="chip-container">
                    <span class="kw-chip chip-tech">Python</span>
                    <span class="kw-chip chip-tech">TypeScript</span>
                    <span class="kw-chip chip-tech">FastAPI</span>
                    <span class="kw-chip chip-tech">React / Next.js</span>
                    <span class="kw-chip chip-tech">Node.js</span>
                    <span class="kw-chip chip-tech">Go</span>
                    <span class="kw-chip chip-tech">GraphQL</span>
                </div>
                <div class="group-heading" style="color: #0369a1; margin-top: 8px;">☁️ Cloud, DevOps & Databases</div>
                <div class="chip-container">
                    <span class="kw-chip chip-tech">Docker</span>
                    <span class="kw-chip chip-tech">Kubernetes</span>
                    <span class="kw-chip chip-tech">PostgreSQL</span>
                    <span class="kw-chip chip-tech">AWS (Lambda / S3)</span>
                    <span class="kw-chip chip-tech">GCP</span>
                    <span class="kw-chip chip-tech">CI/CD Pipelines</span>
                    <span class="kw-chip chip-tech">Microservices</span>
                    <span class="kw-chip chip-tech">Terraform</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            """
            <div class="category-card" style="border-top: 3.5px solid #16a34a !important;">
                <div class="group-heading" style="color: #15803d;">📈 Executive & Financial Leadership</div>
                <div class="chip-container">
                    <span class="kw-chip chip-biz">P&L Management</span>
                    <span class="kw-chip chip-biz">Revenue Growth</span>
                    <span class="kw-chip chip-biz">Budget Forecasting</span>
                    <span class="kw-chip chip-biz">Stakeholder Alignment</span>
                    <span class="kw-chip chip-biz">M&A Strategy</span>
                    <span class="kw-chip chip-biz">Risk Mitigation</span>
                </div>
                <div class="group-heading" style="color: #15803d; margin-top: 8px;">⚙️ Operations & Process Optimization</div>
                <div class="chip-container">
                    <span class="kw-chip chip-biz">Cross-Functional Leadership</span>
                    <span class="kw-chip chip-biz">Process Automation</span>
                    <span class="kw-chip chip-biz">KPI Dashboards</span>
                    <span class="kw-chip chip-biz">Change Management</span>
                    <span class="kw-chip chip-biz">Vendor Relations</span>
                    <span class="kw-chip chip-biz">Six Sigma</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            """
            <div class="category-card" style="border-top: 3.5px solid #ea580c !important;">
                <div class="group-heading" style="color: #c2410c;">🎯 Product Strategy & Discovery</div>
                <div class="chip-container">
                    <span class="kw-chip chip-pm">Roadmap Prioritization</span>
                    <span class="kw-chip chip-pm">User Journey Mapping</span>
                    <span class="kw-chip chip-pm">Product-Led Growth (PLG)</span>
                    <span class="kw-chip chip-pm">Market Validation</span>
                    <span class="kw-chip chip-pm">Competitive Analysis</span>
                    <span class="kw-chip chip-pm">Feature Scoping</span>
                </div>
                <div class="group-heading" style="color: #c2410c; margin-top: 8px;">📊 Analytics & Agile Delivery</div>
                <div class="chip-container">
                    <span class="kw-chip chip-pm">A/B Testing</span>
                    <span class="kw-chip chip-pm">SQL Analytics</span>
                    <span class="kw-chip chip-pm">Agile / Scrum</span>
                    <span class="kw-chip chip-pm">Sprint Planning</span>
                    <span class="kw-chip chip-pm">Release Management</span>
                    <span class="kw-chip chip-pm">Cohort Retention</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab4:
        st.markdown(
            """
            <div class="category-card" style="border-top: 3.5px solid #c026d3 !important;">
                <div class="group-heading" style="color: #a21caf;">🎨 UI Design & Systems</div>
                <div class="chip-container">
                    <span class="kw-chip chip-ux">Figma</span>
                    <span class="kw-chip chip-ux">Design Systems</span>
                    <span class="kw-chip chip-ux">Interactive Prototyping</span>
                    <span class="kw-chip chip-ux">Wireframing</span>
                    <span class="kw-chip chip-ux">Design Tokens</span>
                    <span class="kw-chip chip-ux">Micro-Interactions</span>
                </div>
                <div class="group-heading" style="color: #a21caf; margin-top: 8px;">🔬 Research & Accessibility</div>
                <div class="chip-container">
                    <span class="kw-chip chip-ux">Usability Testing</span>
                    <span class="kw-chip chip-ux">User Research Interviews</span>
                    <span class="kw-chip chip-ux">Information Architecture</span>
                    <span class="kw-chip chip-ux">WCAG 2.1 Accessibility</span>
                    <span class="kw-chip chip-ux">Heuristic Evaluation</span>
                    <span class="kw-chip chip-ux">Card Sorting</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='glass-divider'></div>", unsafe_allow_html=True)

    # --- Section: Template Kit ---
    st.markdown(
        """
        <div class="section-heading">ATS-Compliant Master Templates</div>
        <p class="section-caption">Pre-formatted single-column baseline files ready for download and editing.</p>
        """,
        unsafe_allow_html=True,
    )

    t1, t2, t3 = st.columns([1, 1, 1], gap="medium")

    with t1:
        st.markdown(
            """
            <div class="template-box-glass">
                <div>
                    <div style="font-size: 1.8rem; margin-bottom: 6px;">💻</div>
                    <div class="template-title">Technical SWE Template</div>
                    <p class="template-subtitle">Organized for repository links, engineering metrics, and tech stacks.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("Coming Soon", key="btn_tech_down", use_container_width=True)

    with t2:
        st.markdown(
            """
            <div class="template-box-glass">
                <div>
                    <div style="font-size: 1.8rem; margin-bottom: 6px;">📊</div>
                    <div class="template-title">Business & Operations</div>
                    <p class="template-subtitle">Designed for strategic leadership trajectory, budget scopes, and P&L metrics.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("Coming Soon", key="btn_biz_down", use_container_width=True)

    with t3:
        st.markdown(
            """
            <div class="template-box-glass">
                <div>
                    <div style="font-size: 1.8rem; margin-bottom: 6px;">🚀</div>
                    <div class="template-title">Product & Growth</div>
                    <p class="template-subtitle">Focuses on feature ownership, A/B test outcomes, and user growth data.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("Coming Soon", key="btn_pm_down", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)