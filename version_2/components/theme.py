"""
Enterprise Premium Design System for Streamlit
================================================
A visually stunning, trust-building design with gradients,
glassmorphism, micro-animations, and rich color accents.

Design Philosophy:
    - Deep gradient backgrounds for depth
    - Glassmorphism cards with backdrop-blur
    - Animated accent lines and hover effects
    - Rich blue-to-violet gradient palette
    - Professional yet visually impressive
"""

import streamlit as st

def inject_enterprise_theme():
    """Inject Premium Enterprise CSS into the Streamlit app."""
    st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)

ENTERPRISE_CSS = """
<style>
/* =========================================================
   ENTERPRISE PREMIUM DESIGN SYSTEM
   ========================================================= */

/* --- 1. FONTS & ANIMATIONS --- */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 4px rgba(99,102,241,0.4); }
    50% { box-shadow: 0 0 12px rgba(99,102,241,0.7); }
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

:root {
    /* Gradient Palette */
    --ent-gradient-primary: linear-gradient(135deg, #1E293B 0%, #334155 50%, #1E293B 100%);
    --ent-gradient-accent:  linear-gradient(135deg, #2563EB 0%, #7C3AED 50%, #2563EB 100%);
    --ent-gradient-accent-h: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
    --ent-gradient-warm:    linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
    --ent-gradient-cool:    linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
    --ent-gradient-sidebar:  linear-gradient(180deg, #0F172A 0%, #1E293B 40%, #0F172A 100%);

    /* Core Colors */
    --ent-navy:           #0F172A;
    --ent-navy-mid:       #1E293B;
    --ent-navy-light:     #334155;
    --ent-bg:             #F8FAFC;
    --ent-bg-card:        #FFFFFF;
    --ent-bg-glass:       rgba(255,255,255,0.7);
    --ent-bg-hover:       #F1F5F9;
    --ent-border:         #E2E8F0;
    --ent-border-focus:   #CBD5E1;
    --ent-text:           #0F172A;
    --ent-text-secondary: #1E293B;
    --ent-text-muted:     #475569;
    --ent-accent:         #2563EB;
    --ent-accent-hover:   #1D4ED8;
    --ent-accent-light:   #DBEAFE;
    --ent-violet:         #7C3AED;
    --ent-violet-light:   #EDE9FE;
    --ent-success:        #059669;
    --ent-success-bg:     #ECFDF5;
    --ent-error:          #DC2626;
    --ent-error-bg:       #FEF2F2;
    --ent-warning:        #D97706;
    --ent-warning-bg:     #FFFBEB;
    --ent-radius:         8px;
    --ent-radius-lg:      12px;
    --ent-radius-xl:      16px;
    --ent-shadow-sm:      0 1px 2px rgba(0,0,0,0.04);
    --ent-shadow:         0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --ent-shadow-md:      0 4px 6px -1px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.04);
    --ent-shadow-lg:      0 10px 25px -5px rgba(0,0,0,0.08), 0 4px 10px rgba(0,0,0,0.04);
    --ent-shadow-xl:      0 20px 40px -10px rgba(0,0,0,0.12);
    --ent-shadow-glow:    0 0 20px rgba(37,99,235,0.15);
    --ent-transition:     all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    --ent-transition-slow: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

html, body, [class*="css"] {
    font-family: 'Pretendard', 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    color: var(--ent-text) !important;
}

/* --- 2. APP BACKGROUND --- */
.stApp {
    background: #FFFFFF !important;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
    animation: fadeInUp 0.4s ease-out;
}

/* --- 3. TYPOGRAPHY --- */
h1 {
    font-weight: 800 !important;
    font-size: 1.8rem !important;
    letter-spacing: -0.03em !important;
    color: var(--ent-navy) !important;
    margin-bottom: 0.25rem !important;
    line-height: 1.2 !important;
}
h2 {
    font-weight: 700 !important;
    font-size: 1.3rem !important;
    letter-spacing: -0.02em !important;
    color: var(--ent-navy-mid) !important;
    line-height: 1.3 !important;
}
h3 {
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    letter-spacing: -0.01em !important;
    color: var(--ent-navy-mid) !important;
    line-height: 1.4 !important;
}
p, span, label, .stMarkdown, div {
    color: #0F172A !important;
    line-height: 1.65;
}
.stCaption, small, .stCaption p {
    color: #334155 !important;
    font-size: 0.82rem !important;
}

/* --- 4. SIDEBAR (Gradient Navy) --- */
section[data-testid="stSidebar"] {
    background: var(--ent-gradient-sidebar) !important;
    border-right: none !important;
    box-shadow: 4px 0 15px rgba(0,0,0,0.1);
}

/* Subtle pattern overlay */
section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(circle at 20% 20%, rgba(37,99,235,0.06) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(124,58,237,0.04) 0%, transparent 50%);
    pointer-events: none;
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] label {
    color: #F1F5F9 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin: 0.75rem 0 !important;
}

/* Sidebar Buttons — Glass style */
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.08) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: var(--ent-radius) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.7rem !important;
    transition: var(--ent-transition) !important;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.2) !important;
    color: #FFFFFF !important;
    transform: none !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}

/* Sidebar Inputs — Glass */
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #FFFFFF !important;
    border-radius: var(--ent-radius) !important;
    font-size: 0.82rem !important;
    backdrop-filter: blur(4px);
}
section[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
section[data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
    color: #94A3B8 !important;
}

/* Sidebar Select */
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #FFFFFF !important;
    border-radius: var(--ent-radius) !important;
}

/* Sidebar Download */
section[data-testid="stSidebar"] .stDownloadButton > button {
    background: transparent !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    font-size: 0.78rem !important;
}
section[data-testid="stSidebar"] .stDownloadButton > button:hover {
    color: #E2E8F0 !important;
    border-color: rgba(255,255,255,0.15) !important;
    background: rgba(255,255,255,0.05) !important;
}

/* Sidebar alert boxes */
section[data-testid="stSidebar"] .stInfo,
section[data-testid="stSidebar"] .stWarning,
section[data-testid="stSidebar"] .stSuccess {
    font-size: 0.72rem !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #CBD5E1 !important;
}

/* --- 5. BUTTONS (Main Area) --- */
/* Primary — Gradient Navy Button */
.stButton > button {
    background: linear-gradient(135deg, #1E293B 0%, #334155 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: var(--ent-radius) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.25rem !important;
    transition: var(--ent-transition) !important;
    box-shadow: var(--ent-shadow-md) !important;
    cursor: pointer !important;
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    transition: left 0.5s ease;
}
.stButton > button:hover::before {
    left: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
    box-shadow: var(--ent-shadow-lg), var(--ent-shadow-glow) !important;
    transform: translateY(-2px);
}
.stButton > button:active {
    transform: translateY(0);
    box-shadow: var(--ent-shadow-sm) !important;
}

/* Disabled */
.stButton > button:disabled {
    background: #E2E8F0 !important;
    color: #1E293B !important;
    border: 1px solid #CBD5E1 !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}
.stButton > button:disabled::before {
    display: none;
}

/* Download Button — Blue Outline with glow */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--ent-accent) !important;
    border: 1.5px solid var(--ent-accent) !important;
    border-radius: var(--ent-radius) !important;
    font-weight: 600 !important;
    transition: var(--ent-transition) !important;
    position: relative;
}
.stDownloadButton > button:hover {
    background: var(--ent-accent-light) !important;
    border-color: var(--ent-accent-hover) !important;
    color: var(--ent-accent-hover) !important;
    box-shadow: 0 0 15px rgba(37,99,235,0.15) !important;
    transform: translateY(-1px);
}

/* --- 6. TEXT INPUTS --- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #FFFFFF !important;
    color: var(--ent-text) !important;
    border: 1.5px solid var(--ent-border) !important;
    border-radius: var(--ent-radius) !important;
    padding: 0.6rem 0.9rem !important;
    font-size: 0.875rem !important;
    transition: var(--ent-transition) !important;
    box-shadow: var(--ent-shadow-sm) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--ent-accent) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1), var(--ent-shadow-sm) !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--ent-text-muted) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid var(--ent-border) !important;
    border-radius: var(--ent-radius) !important;
    color: var(--ent-text) !important;
    box-shadow: var(--ent-shadow-sm) !important;
    transition: var(--ent-transition) !important;
}
.stSelectbox > div > div:hover {
    border-color: var(--ent-border-focus) !important;
}

/* --- 7. TABS --- */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--ent-border) !important;
    gap: 0 !important;
    padding: 0 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--ent-text-muted) !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    transition: var(--ent-transition) !important;
    border-radius: 0 !important;
    margin-bottom: -2px !important;
    position: relative;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--ent-navy-mid) !important;
    background: linear-gradient(180deg, transparent 80%, rgba(37,99,235,0.04) 100%) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--ent-accent) !important;
    border-bottom: 3px solid var(--ent-accent) !important;
    background: transparent !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
    animation: fadeInUp 0.3s ease-out;
}

/* --- 8. CARDS / EXPANDERS --- */
div[data-testid="stExpander"] {
    background: var(--ent-bg-glass) !important;
    border: 1px solid var(--ent-border) !important;
    border-radius: var(--ent-radius-lg) !important;
    box-shadow: var(--ent-shadow) !important;
    overflow: hidden;
    transition: var(--ent-transition) !important;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}
div[data-testid="stExpander"]:hover {
    box-shadow: var(--ent-shadow-md) !important;
    border-color: var(--ent-border-focus) !important;
    transform: translateY(-1px);
}
div[data-testid="stExpander"] summary {
    color: #0F172A !important;
    font-weight: 700 !important;
}

/* --- 9. DATA EDITOR / TABLE --- */
.stDataFrame, div[data-testid="stDataFrame"] {
    border: 1px solid var(--ent-border) !important;
    border-radius: var(--ent-radius-lg) !important;
    overflow: hidden;
    box-shadow: var(--ent-shadow) !important;
}

div[data-testid="stDataFrame"] th,
div[data-testid="stDataFrame"] [role="columnheader"] {
    background: linear-gradient(180deg, #F1F5F9, #E8EDF2) !important;
    color: #0F172A !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    border-bottom: 2px solid var(--ent-border) !important;
    padding: 0.7rem 0.8rem !important;
}

div[data-testid="stDataFrame"] td,
div[data-testid="stDataFrame"] [role="gridcell"] {
    font-size: 0.84rem !important;
    color: #0F172A !important;
    border-bottom: 1px solid #F1F5F9 !important;
}

/* --- 10. METRIC CARDS (Premium) --- */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--ent-border);
    border-radius: var(--ent-radius-lg);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--ent-shadow);
    transition: var(--ent-transition-slow);
    position: relative;
    overflow: hidden;
}
div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2563EB, #7C3AED, #2563EB);
    background-size: 200% 100%;
    animation: gradient-shift 3s ease infinite;
}
div[data-testid="stMetric"]:hover {
    box-shadow: var(--ent-shadow-lg);
    transform: translateY(-2px);
    border-color: var(--ent-border-focus);
}
div[data-testid="stMetric"] label {
    color: #1E293B !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--ent-navy) !important;
    font-weight: 800 !important;
    font-size: 1.75rem !important;
}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}

/* --- 11. ALERTS --- */
div[data-testid="stAlert"] {
    border-radius: var(--ent-radius) !important;
    font-size: 0.85rem !important;
    animation: fadeInUp 0.3s ease-out;
}
.stSuccess {
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5) !important;
    color: #065F46 !important;
    border: 1px solid #A7F3D0 !important;
    border-radius: var(--ent-radius) !important;
}
.stError {
    background: linear-gradient(135deg, #FEF2F2, #FEE2E2) !important;
    color: #991B1B !important;
    border: 1px solid #FECACA !important;
    border-radius: var(--ent-radius) !important;
}
.stWarning {
    background: linear-gradient(135deg, #FFFBEB, #FEF3C7) !important;
    color: #92400E !important;
    border: 1px solid #FDE68A !important;
    border-radius: var(--ent-radius) !important;
}
.stInfo {
    background: linear-gradient(135deg, #EFF6FF, #DBEAFE) !important;
    color: #1E40AF !important;
    border: 1px solid #BFDBFE !important;
    border-radius: var(--ent-radius) !important;
}

/* --- 12. DIVIDERS --- */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, #E2E8F0, transparent) !important;
    margin: 1.5rem 0 !important;
}

/* --- 13. LINKS --- */
a {
    color: var(--ent-accent) !important;
    text-decoration: none !important;
    font-weight: 500;
    transition: var(--ent-transition);
    position: relative;
}
a:hover {
    color: var(--ent-violet) !important;
}

/* --- 14. TOAST --- */
div[data-testid="stToast"] {
    background: var(--ent-bg-card) !important;
    color: var(--ent-text) !important;
    border: 1px solid var(--ent-border) !important;
    border-radius: var(--ent-radius-lg) !important;
    box-shadow: var(--ent-shadow-xl) !important;
    animation: fadeInUp 0.3s ease-out;
}

/* --- 15. SCROLLBAR --- */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #CBD5E1, #94A3B8);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #94A3B8, #64748B);
}

/* --- 16. SPINNER --- */
.stSpinner > div {
    border-top-color: var(--ent-accent) !important;
}

</style>
"""


# ---------------------------------------------------------------
#  PREMIUM HTML COMPONENTS
# ---------------------------------------------------------------

def render_enterprise_header(title: str, subtitle: str = ""):
    """Premium hero header — large icon, bold title, gradient accent."""
    subtitle_html = f'<p style="color:#475569;font-size:1rem;margin:8px 0 0 0;font-weight:400;letter-spacing:-0.01em;">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
        <div style="
            padding: 2.5rem 0 2rem 0;
            border-bottom: 2px solid #E2E8F0;
            margin-bottom: 2rem;
            position: relative;
        ">
            <div style="
                position:absolute; bottom:-2px; left:0;
                width:120px; height:3px;
                background: linear-gradient(90deg, #2563EB, #7C3AED);
                border-radius: 2px;
            "></div>
            <div style="display:flex;align-items:center;gap:18px;margin-bottom:4px;">
                <div style="
                    width:52px;height:52px;
                    background: linear-gradient(135deg, #1E293B, #334155);
                    border-radius: 14px;
                    display:flex;align-items:center;justify-content:center;
                    box-shadow: 0 4px 14px rgba(30,41,59,0.3);
                    flex-shrink:0;
                ">
                    <div style="
                        width:22px;height:22px;
                        background:#fff;
                        clip-path: polygon(50% 5%, 97% 95%, 3% 95%);
                    "></div>
                </div>
                <div>
                    <h1 style="
                        margin:0 !important;padding:0 !important;
                        font-size:2.2rem !important;font-weight:800 !important;
                        letter-spacing:-0.04em !important;
                        background: linear-gradient(135deg, #0F172A 30%, #334155 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        line-height:1.1 !important;
                    ">{title}</h1>
                    {subtitle_html}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = "", trend: str = "up", accent: str = "blue"):
    """Premium metric card with gradient top bar and animated hover."""
    delta_color = "#059669" if trend == "up" else "#DC2626"
    delta_icon = "↑" if trend == "up" else "↓"
    delta_html = f'<span style="color:{delta_color};font-size:0.82rem;font-weight:600;">{delta_icon} {delta}</span>' if delta else ""

    gradients = {
        "blue": "linear-gradient(135deg, #2563EB, #3B82F6)",
        "violet": "linear-gradient(135deg, #7C3AED, #8B5CF6)",
        "cyan": "linear-gradient(135deg, #0891B2, #06B6D4)",
        "amber": "linear-gradient(135deg, #D97706, #F59E0B)",
    }
    bar_gradient = gradients.get(accent, gradients["blue"])

    st.markdown(f"""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.boxShadow='0 8px 25px rgba(0,0,0,0.1)';this.style.transform='translateY(-3px)'"
           onmouseout="this.style.boxShadow='0 1px 3px rgba(0,0,0,0.06)';this.style.transform='translateY(0)'">
            <div style="
                position:absolute;top:0;left:0;right:0;height:3px;
                background:{bar_gradient};
            "></div>
            <p style="
                color:#64748B;font-size:0.7rem;font-weight:700;
                text-transform:uppercase;letter-spacing:0.08em;
                margin:0 0 10px 0;
            ">{label}</p>
            <div style="display:flex;align-items:baseline;gap:10px;">
                <span style="
                    color:#0F172A;font-size:2rem;font-weight:800;
                    letter-spacing:-0.03em;line-height:1;
                ">{value}</span>
                {delta_html}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, description: str = ""):
    """Section header with accent dot."""
    desc_html = f'<p style="color:#64748B;font-size:0.85rem;margin:4px 0 0 0;">{description}</p>' if description else ""
    st.markdown(f"""
        <div style="margin-bottom:1.25rem;">
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="
                    width:8px; height:8px;
                    background: linear-gradient(135deg, #2563EB, #7C3AED);
                    border-radius: 50%;
                "></div>
                <h3 style="
                    margin:0 !important;
                    color:#1E293B !important;
                    font-size:1.05rem !important;
                    font-weight:700 !important;
                ">{title}</h3>
            </div>
            {desc_html}
        </div>
    """, unsafe_allow_html=True)


def render_info_banner(text: str, accent: str = "blue"):
    """Colored info banner with gradient left border."""
    colors = {
        "blue":   ("#EFF6FF", "#2563EB"),
        "violet": ("#EDE9FE", "#7C3AED"),
        "green":  ("#ECFDF5", "#059669"),
        "amber":  ("#FFFBEB", "#D97706"),
    }
    bg, border = colors.get(accent, colors["blue"])
    st.markdown(f"""
        <div style="
            background: {bg};
            border-left: 4px solid {border};
            border-radius: 0 8px 8px 0;
            padding: 0.9rem 1.2rem;
            margin: 0.75rem 0;
            font-size: 0.85rem;
            color: #334155;
            line-height: 1.6;
        ">{text}</div>
    """, unsafe_allow_html=True)
