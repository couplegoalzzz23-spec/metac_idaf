import streamlit as st

# ==============================================================================
# 1. SHIELD LAYER (Penting: Jangan dihapus)
# Mematikan fungsi st.set_page_config dari modul turunan agar tidak crash
# ==============================================================================
if 'original_set_page_config' not in st.__dict__:
    st.original_set_page_config = st.set_page_config
    st.set_page_config = lambda *args, **kwargs: None

st.original_set_page_config(
    page_title="Integrated Aviation Weather Center",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 1.5 PRESENTATION LAYER (Global CSS Injection - Military & Bloomberg Theme)
# Diletakkan di atas agar mengunci desain secara global tanpa mengubah fungsi
# ==============================================================================
st.markdown("""
    <style>
    /* GLOBAL TYPOGRAPHY */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
    }

    /* DARK MODE OVERRIDES (Sesuai Spesifikasi Mutlak) */
    @media (prefers-color-scheme: dark) {
        /* Background & Secondary */
        .stApp, .stApp > header {
            background-color: #0F172A !important;
        }
        [data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid rgba(255,255,255,0.08) !important;
        }
        [data-testid="stSidebarNav"] {
            background-color: #111827 !important;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6, div[data-testid="stMetricValue"] {
            color: #F8FAFC !important;
        }
        p, .stMarkdown, .stText, span, div[data-testid="stMetricLabel"] {
            color: #CBD5E1 !important;
        }
        
        /* Cards & Metric Premium */
        .css-1r6slb0, .css-12oz5g7, [data-testid="stMetric"], .stCard, div[data-testid="stExpander"] {
            background-color: #1E293B !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 18px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        [data-testid="stMetric"]:hover, .stCard:hover {
            transform: translateY(-5px);
            border-color: #38BDF8 !important;
            box-shadow: 0 12px 24px rgba(0,0,0,0.5) !important;
        }
        
        /* Accents & Highlights */
        .st-bb, .st-cb, a, .st-emotion-cache-1104q0 {
            color: #38BDF8 !important;
        }
    }

    /* FLOATING & ANIMATED SIDEBAR NAVIGATION */
    [data-testid="stSidebarNav"] ul li div {
        border-radius: 8px !important;
        margin: 4px 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    [data-testid="stSidebarNav"] ul li div:hover {
        background-color: rgba(56, 189, 248, 0.1) !important;
        transform: translateX(6px);
    }
    
    /* HERO SECTION STYLING (Glassmorphism & Gradient) */
    .hero-panel {
        background: linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(30,41,59,0.98) 100%);
        padding: 3rem;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 12px 40px rgba(0,0,0,0.25);
        margin-top: -1rem;
        margin-bottom: 2rem;
        position: relative;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: rgba(34, 197, 94, 0.1);
        color: #22C55E;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1px;
        border: 1px solid rgba(34, 197, 94, 0.2);
        margin-bottom: 1.5rem;
    }
    
    .status-dot {
        width: 8px; height: 8px;
        background-color: #22C55E;
        border-radius: 50%;
        box-shadow: 0 0 12px #22C55E;
        animation: radar-pulse 2s infinite;
    }
    
    @keyframes radar-pulse {
        0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
        100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DEFINISI HALAMAN
# ==============================================================================
def show_home():
    # Hero Section Redesign (Presentation Layer Only)
    import datetime
    last_update = datetime.datetime.utcnow().strftime("%d %b %Y • %H:%M UTC")
    
    st.markdown(f"""
    <div class="hero-panel">
        <div class="status-badge">
            <div class="status-dot"></div>
            SYSTEM SECURE • ONLINE
        </div>
        <h1 style="font-size: 2.8rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.1; color: #F8FAFC;">
            Integrated Aviation <br><span style="color: #38BDF8;">Weather Center</span>
        </h1>
        <p style="color: #CBD5E1; font-size: 1.15rem; max-width: 700px; margin-bottom: 1.5rem; line-height: 1.6;">
            Tactical Meteorological Command System berjalan secara stabil. Menggunakan arsitektur Multi-Page untuk visualisasi data cuaca presisi tinggi.
        </p>
        <p style="color: #475569; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">
            ⏱️ ZULU LAST SYNC: {last_update}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. SISTEM ROUTING MODERN (Streamlit >= 1.35)
# (Logika Routing 100% Asli Tidak Diubah)
# ==============================================================================
# Gunakan st.Page untuk membaca file .py secara langsung
page_home = st.Page(show_home, title="Home", icon="🏠", default=True)
page_metar = st.Page("metar_dashboard.py", title="Real-Time Weather", icon="📡")
page_diurnal = st.Page("meteogram_dashboard.py", title="Diurnal Meteogram", icon="📈")
page_acs = st.Page("acs_dashboard.py", title="ACS Climatology", icon="📊")

# Konfigurasi Navigasi Sidebar
nav = st.navigation({
    "MAIN COMMAND": [page_home],
    "METEOROLOGICAL CORE": [page_metar, page_diurnal, page_acs]
})

# Jalankan Router
nav.run()
