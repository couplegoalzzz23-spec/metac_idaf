import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 1. SHIELD LAYER (PENTING: Jangan Dihapus)
# Melumpuhkan fungsi st.set_page_config dari modul turunan agar tidak crash
# ==============================================================================
if 'original_set_page_config' not in st.__dict__:
    st.original_set_page_config = st.set_page_config
    st.set_page_config = lambda *args, **kwargs: None

# Konfigurasi Utama Command Center
st.original_set_page_config(
    page_title="Integrated Aviation Weather Center",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. DEFINISI HALAMAN KUSTOM & PRESENTATION LAYER (UI/UX)
# ==============================================================================
def show_home():
    # Waktu Sistem Real-Time
    current_time = datetime.utcnow().strftime("%d %b %Y • %H:%M UTC")

    # CSS INJECTION - ENTERPRISE MILITARY GRADE DASHBOARD
    st.markdown("""
        <style>
        /* === GLOBAL TYPOGRAPHY === */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        .stApp {
            font-family: 'Inter', -apple-system, sans-serif;
        }

        /* === LIGHT MODE VARIABLES (Refined & Maintained) === */
        :root {
            --bg-main: #F8FAFC;
            --card-bg: #FFFFFF;
            --card-glass: rgba(255, 255, 255, 0.85);
            --text-primary: #0F172A;
            --text-secondary: #475569;
            --accent: #328CC1;
            --border-color: rgba(15, 23, 42, 0.08);
            --shadow-sm: 0 4px 6px rgba(0, 0, 0, 0.04);
            --shadow-lg: 0 10px 40px rgba(0, 0, 0, 0.08);
            --success: #16A34A;
        }

        /* === DARK MODE VARIABLES (Total Redesign) === */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-main: #0F172A;
                --card-bg: #1E293B;
                --card-glass: rgba(30, 41, 59, 0.75);
                --text-primary: #F8FAFC;
                --text-secondary: #CBD5E1;
                --accent: #38BDF8;
                --border-color: rgba(255, 255, 255, 0.08);
                --shadow-sm: 0 4px 6px rgba(0, 0, 0, 0.3);
                --shadow-lg: 0 10px 40px rgba(0, 0, 0, 0.5);
                --success: #22C55E;
            }
        }

        /* === NATIVE STREAMLIT OVERRIDES === */
        .stApp {
            background-color: var(--bg-main);
        }
        
        /* Floating & Rounded Sidebar */
        [data-testid="stSidebar"] {
            background-color: var(--card-bg) !important;
            border-right: 1px solid var(--border-color) !important;
            box-shadow: 4px 0 24px rgba(0,0,0,0.02);
        }
        
        [data-testid="stSidebarNav"] ul li div {
            border-radius: 8px !important;
            margin: 4px 12px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        [data-testid="stSidebarNav"] ul li div:hover {
            background-color: rgba(56, 189, 248, 0.1) !important;
            transform: translateX(4px);
        }
        
        [data-testid="stSidebarNav"] ul li div[data-testid="stSidebarNavLinkActive"] {
            background-color: rgba(56, 189, 248, 0.15) !important;
            border-left: 4px solid var(--accent) !important;
        }

        /* Sembunyikan garis header default agar lebih bersih */
        hr { display: none; }

        /* === HERO SECTION (Glassmorphism & Aviation Theme) === */
        .hero-container {
            background: linear-gradient(135deg, rgba(11, 60, 93, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%), 
                        url('https://images.unsplash.com/photo-1544015759-22cbdd1bd09d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80') center/cover;
            padding: 3rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border-color);
            margin-top: -1rem;
        }

        .hero-glass {
            background: var(--card-glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 2.5rem;
            border-radius: 18px;
            border: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
        }

        /* Status Indicator (Online Radar Style) */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: rgba(34, 197, 94, 0.1);
            color: var(--success);
            padding: 8px 18px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 0.85rem;
            letter-spacing: 1px;
            border: 1px solid rgba(34, 197, 94, 0.2);
            width: fit-content;
        }
        
        .status-dot {
            width: 8px; height: 8px;
            background-color: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 12px var(--success);
            animation: radar-pulse 2s infinite;
        }

        @keyframes radar-pulse {
            0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
            100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }

        /* Typography Hierarchy */
        .hero-title {
            color: var(--text-primary) !important;
            font-size: 2.7rem !important;
            font-weight: 800 !important;
            margin: 0 !important;
            line-height: 1.1 !important;
            letter-spacing: -1px;
        }
        
        .hero-title span {
            color: var(--accent);
        }

        .hero-subtitle {
            color: var(--text-secondary) !important;
            font-size: 1.15rem;
            font-weight: 400;
            margin: 0;
            max-width: 850px;
            line-height: 1.7;
        }

        /* === METRIC CARDS (Bloomberg / Enterprise Style) === */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .metric-card {
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 18px;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-sm);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 1.2rem;
            position: relative;
            overflow: hidden;
            cursor: default;
        }

        /* Gradient Border on Hover */
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 4px; height: 100%;
            background: linear-gradient(180deg, var(--accent) 0%, transparent 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
            border-color: var(--accent);
        }

        .metric-card:hover::before {
            opacity: 1;
        }

        .metric-icon {
            font-size: 2.2rem;
            background: rgba(56, 189, 248, 0.08);
            width: 55px; height: 55px;
            display: flex; align-items: center; justify-content: center;
            border-radius: 14px;
            color: var(--accent);
        }

        .metric-info h4 {
            color: var(--text-secondary);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin: 0 0 4px 0;
            font-weight: 600;
        }

        .metric-info h2 {
            color: var(--text-primary);
            font-size: 1.4rem;
            margin: 0;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # RENDER HERO SECTION & DASHBOARD METRICS
    # ==============================================================================
    st.markdown(f"""
        <div class="hero-container">
            <div class="hero-glass">
                <div class="status-badge">
                    <div class="status-dot"></div>
                    SYSTEM SECURE • ONLINE
                </div>
                
                <h1 class="hero-title">Integrated Aviation<br><span>Weather Center</span></h1>
                
                <p class="hero-subtitle">
                    Tactical Meteorological Command System terintegrasi dengan arsitektur <b>Multi-Page Isolated Node</b>. 
                    Mendukung pengambilan keputusan komando berbasis visualisasi data real-time, sinoptik, dan klimatologi presisi tinggi.
                </p>

                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-icon">📡</div>
                        <div class="metric-info">
                            <h4>Tactical METAR</h4>
                            <h2>Active Node</h2>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">📈</div>
                        <div class="metric-info">
                            <h4>Diurnal Synoptic</h4>
                            <h2>Active Node</h2>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">📊</div>
                        <div class="metric-info">
                            <h4>ACS Climatology</h4>
                            <h2>Active Node</h2>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">⏱️</div>
                        <div class="metric-info">
                            <h4>ZULU Sync Time</h4>
                            <h2>{current_time}</h2>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. SISTEM ROUTING MODERN (Streamlit >= 1.35) - [LOCKED]
# ==============================================================================
# Definisi objek halaman (membaca file eksternal tanpa memodifikasi isinya)
page_home = st.Page(show_home, title="Beranda Utama", icon="🏠", default=True)
page_metar = st.Page("metar_dashboard.py", title="Real-Time Weather", icon="📡")
page_diurnal = st.Page("meteogram_dashboard.py", title="Diurnal Meteogram", icon="📈")
page_acs = st.Page("acs_dashboard.py", title="ACS Climatology", icon="📊")

# Konfigurasi Navigasi Sidebar secara terstruktur
nav = st.navigation({
    "MAIN COMMAND": [page_home],
    "METEOROLOGICAL CORE": [page_metar, page_diurnal, page_acs]
})

# Eksekusi sistem navigasi
nav.run()
