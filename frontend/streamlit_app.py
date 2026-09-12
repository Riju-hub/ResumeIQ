import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from frontend.services.api_client import health_check

st.set_page_config(
    page_title="ResumeIQ — AI Powered ATS Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 1. State Initialization
for key, default in [
    ("access_token", None),
    ("refresh_token", None),
    ("user_id", None),
    ("user_email", None),
    ("auth_error", None),
    ("auth_info", None),
    ("auth_mode", "signin"),
    ("current_view", "landing"),
    ("oauth_processed", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# 2. Safe Google OAuth Redirect Handler
if (
    not st.session_state.access_token 
    and "code" in st.query_params 
    and not st.session_state.oauth_processed
):
    st.session_state.oauth_processed = True
    auth_code = st.query_params.get("code")
    st.query_params.clear()
    
    if auth_code:
        try:
            from frontend.services import supabase_client
            result = supabase_client.exchange_code_for_session(auth_code)
            if "error" in result:
                st.session_state.auth_error = f"Sign-in error: {result['error']}"
            else:
                st.session_state.access_token = result.get("access_token")
                st.session_state.refresh_token = result.get("refresh_token")
                st.session_state.user_id = result.get("user_id")
                st.session_state.user_email = result.get("email")
                st.rerun()
        except Exception as exc:
            st.session_state.auth_error = f"Authentication error: {exc}"

def load_css():
    try:
        css_path = Path(__file__).resolve().parent / "assets" / "styles.css"
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                return f"<style>{f.read()}</style>"
    except Exception:
        pass
    return ""

st.markdown(load_css(), unsafe_allow_html=True)

# 3. Modern Design System & Component Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    [data-testid="stSidebar"] {
        background: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #E2E8F0 !important;
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5); }
        70% { box-shadow: 0 0 0 7px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        display: inline-block;
        animation: pulseGlow 2s infinite;
        margin-right: 8px;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 5px 12px;
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 999px;
        color: #047857;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 1.25rem;
    }

    .status-badge-offline {
        display: inline-flex;
        align-items: center;
        padding: 5px 12px;
        background: #FFF1F2;
        border: 1px solid #FECDD3;
        border-radius: 999px;
        color: #BE123C;
        font-size: 0.76rem;
        font-weight: 700;
        margin-bottom: 1.25rem;
    }

    [data-testid="stSidebar"] div.stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        padding: 0.5rem 0.75rem !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #475569 !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    }

    [data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
        background: #F1F5F9 !important;
        color: #0F172A !important;
        border-color: #CBD5E1 !important;
        transform: translateY(-1px);
    }

    [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
    }

    [data-testid="stSidebar"] [data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 1rem 1rem 1.2rem 1rem !important;
        box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.05) !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
        background-color: #FFFFFF !important;
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }

    [data-testid="stSidebar"] input {
        color: #0F172A !important;
        font-size: 0.85rem !important;
    }

    [data-testid="stSidebar"] label p {
        color: #475569 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 2px !important;
    }

    [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1rem !important;
        margin-top: 0.25rem !important;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3) !important;
    }

    [data-testid="stSidebar"] [data-testid="InputInstructions"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=30)
def check_backend_status():
    try:
        res = health_check()
        if isinstance(res, dict) and res.get("status") == "healthy":
            return {"status": "healthy"}
        return {"status": "offline"}
    except Exception:
        return {"status": "offline"}


# 4. Modern Sidebar Layout
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1.15rem;">
            <div style="
                background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
                width: 42px; height: 42px; border-radius: 12px;
                display: flex; align-items: center; justify-content: center;
                box-shadow: 0 6px 18px rgba(79, 70, 229, 0.25);
                flex-shrink: 0;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" fill="white" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.2rem; color: #0F172A; letter-spacing: -0.02em; line-height: 1.1;">
                    Resume<span style="background: linear-gradient(135deg, #4F46E5 0%, #9333EA 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent;">IQ</span>
                </div>
                <div style="font-size: 0.68rem; font-weight: 700; color: #64748B; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 2px;">
                    AI Powered ATS Platform
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Real-Time Telemetry Badge
    status = check_backend_status()
    if status and status.get("status") == "healthy":
        st.markdown('<div class="status-badge"><span class="pulse-dot"></span> ATS Engine Online • Live</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge-offline"><span style="width:8px; height:8px; background:#F43F5E; border-radius:50%; display:inline-block; margin-right:8px;"></span> Engine Offline / Idle</div>', unsafe_allow_html=True)

    # Navigation Section
    st.markdown("<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.08em; color:#64748B; margin-bottom:0.5rem;'>PLATFORM NAVIGATION</div>", unsafe_allow_html=True)
    
    c_nav1, c_nav2 = st.columns(2, gap="small")
    with c_nav1:
        if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.current_view == "landing" else "secondary"):
            st.session_state.current_view = "landing"
            st.rerun()
        if st.button("📊 History", use_container_width=True, type="primary" if st.session_state.current_view == "history" else "secondary"):
            st.session_state.current_view = "history"
            st.rerun()
            
    with c_nav2:
        if st.button("🎯 Scorer", use_container_width=True, type="primary" if st.session_state.current_view == "scorer" else "secondary"):
            st.session_state.current_view = "scorer"
            st.rerun()
        if st.button("📚 Guides", use_container_width=True, type="primary" if st.session_state.current_view == "resources" else "secondary"):
            st.session_state.current_view = "resources"
            st.rerun()

    st.markdown("<hr style='margin: 1.25rem 0; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.08em; color:#64748B; margin-bottom:0.6rem;'>AUTHENTICATION</div>", unsafe_allow_html=True)

    if st.session_state.auth_error:
        st.error(st.session_state.auth_error)
        st.session_state.auth_error = None

    from frontend.services import supabase_client
    if st.session_state.access_token:
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 14px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);">
                <div style="font-size: 0.7rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Active Account</div>
                <div style="font-size: 0.86rem; font-weight: 700; color: #0F172A; word-break: break-all; margin-top: 2px;">
                    {st.session_state.user_email}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🚪 Sign Out", use_container_width=True):
            supabase_client.sign_out()
            for k in ("access_token", "refresh_token", "user_id", "user_email"):
                st.session_state[k] = None
            st.session_state.oauth_processed = False
            st.rerun()
    else:
        col_t1, col_t2 = st.columns(2, gap="small")
        with col_t1:
            if st.button("Sign In", key="btn_auth_signin", use_container_width=True, type="primary" if st.session_state.auth_mode == "signin" else "secondary"):
                st.session_state.auth_mode = "signin"
                st.rerun()
        with col_t2:
            if st.button("Sign Up", key="btn_auth_signup", use_container_width=True, type="primary" if st.session_state.auth_mode == "signup" else "secondary"):
                st.session_state.auth_mode = "signup"
                st.rerun()

        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "signin":
            with st.form("signin_form", clear_on_submit=False):
                email = st.text_input("Email", placeholder="alex@company.com", key="signin_email")
                password = st.text_input("Password", type="password", placeholder="••••••••", key="signin_pw")
                submit_btn = st.form_submit_button("Sign In to Account", use_container_width=True)
                
                if submit_btn:
                    if not email or not password:
                        st.error("Please provide both email and password.")
                    else:
                        res = supabase_client.sign_in_with_password(email.strip(), password.strip())
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.session_state.access_token = res.get("access_token")
                            st.session_state.refresh_token = res.get("refresh_token")
                            st.session_state.user_id = res.get("user_id")
                            st.session_state.user_email = res.get("email")
                            st.rerun()
        else:
            with st.form("signup_form", clear_on_submit=False):
                email_up = st.text_input("Email", placeholder="alex@company.com", key="signup_email")
                password_up = st.text_input("Password", type="password", placeholder="••••••••", key="signup_pw")
                signup_btn = st.form_submit_button("Create Free Account", use_container_width=True)
                
                if signup_btn:
                    if not email_up or not password_up:
                        st.error("Please provide both email and password.")
                    else:
                        res = supabase_client.sign_up_with_password(email_up.strip(), password_up.strip())
                        if "error" in res:
                            st.error(res["error"])
                        elif res.get("pending_confirmation"):
                            st.info("Check your inbox for the confirmation link.")
                        else:
                            st.session_state.access_token = res.get("access_token")
                            st.session_state.refresh_token = res.get("refresh_token")
                            st.session_state.user_id = res.get("user_id")
                            st.session_state.user_email = res.get("email")
                            st.rerun()

# 5. Core View Router
if st.session_state.current_view == 'landing':
    from frontend.views import landing
    landing.render()
elif st.session_state.current_view == 'scorer':
    from frontend.views import scorer
    scorer.render()
elif st.session_state.current_view == 'history':
    from frontend.views import history
    history.render()
elif st.session_state.current_view == 'resources':
    from frontend.views import resources
    resources.render()