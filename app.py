import streamlit as st

# =====================================================================
# 1. BLACK-BOX ISOLATION MONKEY-PATCH (ANTI-CRASH LOGIC)
# Mencegah error duplikasi st.set_page_config() dari sub-halaman
# =====================================================================
if not hasattr(st, '_original_set_page_config'):
    st._original_set_page_config = st.set_page_config
    
    def robust_set_page_config(*args, **kwargs):
        if not st.session_state.get('_page_config_initialized', False):
            st.session_state['_page_config_initialized'] = True
            try:
                st._original_set_page_config(*args, **kwargs)
            except Exception:
                pass
        else:
            pass

    st.set_page_config = robust_set_page_config

# Set konfigurasi inisial pertama kali secara aman sebelum router berjalan
st.set_page_config(
    page_title="U-AWIS | Unified Aviation Weather",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. GLOBAL THEME ENGINE (LIGHT & DARK MODE COALITION)
# =====================================================================
if 'app_theme' not in st.session_state:
    st.session_state.app_theme = 'Dark Mode'

# Membuat floating container di pojok kanan atas layar untuk Theme Switcher
st.markdown("""
    <style>
    .floating-theme-container {
        position: fixed;
        top: 50px;
        right: 20px;
        z-index: 999999;
        background-color: rgba(30, 41, 59, 0.9);
        padding: 5px 15px;
        border-radius: 30px;
        border: 1px solid #334155;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    /* Penyesuaian responsif Streamlit header */
    [data-testid="stHeader"] {
        z-index: 99999;
    }
    </style>
""", unsafe_allow_html=True)

# Render widget pemilih tema secara global di posisi pojok kanan atas
with st.container():
    col_space, col_theme = st.columns([8.5, 1.5])
    with col_theme:
        chosen_theme = st.selectbox(
            "🌓 Tampilan Sistem",
            options=["Dark Mode", "Light Mode"],
            index=0 if st.session_state.app_theme == "Dark Mode" else 1,
            key="global_theme_selector"
        )
        st.session_state.app_theme = chosen_theme

# Aplikasi Skema Warna Berdasarkan Tema yang Dipilih (Mempengaruhi semua sub-dashboard)
if st.session_state.app_theme == "Light Mode":
    st.markdown("""
        <style>
        /* Aplikasi Light Mode Global */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
        }
        [data-testid="stSidebar"] {
            background-color: #E2E8F0 !important;
        }
        h1, h2, h3, h4, h5, h6, .uawis-header h1 {
            color: #1E3A8A !important;
        }
        .uawis-header {
            background: linear-gradient(135deg, #E2E8F0 0%, #CBD5E1 100%) !important;
            border-left: 6px solid #1E3A8A !important;
        }
        .uawis-header p, .stMarkdown, p, span, label {
            color: #334155 !important;
        }
        .module-card {
            background-color: #FFFFFF !important;
            color: #1E293B !important;
            border: 1px solid #CBD5E1 !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        }
        .module-card h3 { color: #B45309 !important; }
        .module-card p { color: #475569 !important; }
        
        /* FIKSASI DROPDOWN READABILITY (Mencegah Teks Putih di Background Putih) */
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
        }
        div[data-baseweb="popover"] li, li[role="option"] {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
        }
        li[role="option"]:hover {
            background-color: #F1F5F9 !important;
        }
        div[data-testid="stMetricValue"] { color: #1E3A8A !important; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        /* Aplikasi Dark Mode Global */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            background-color: #0b0c0c !important;
            color: #cfd2c3 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #111111 !important;
        }
        h1, h2, h3, h4, h5, h6, .uawis-header h1 {
            color: #a9df52 !important;
        }
        .uawis-header {
            background: linear-gradient(135deg, #162A4A 0%, #0D1B2A 100%) !important;
            border-left: 6px solid #00B4D8 !important;
        }
        
        /* FIKSASI DROPDOWN READABILITY DALAM DARK MODE */
        div[data-baseweb="select"] > div {
            background-color: #1E293B !important;
            color: #FFFFFF !important;
        }
        div[data-baseweb="popover"] li, li[role="option"] {
            background-color: #1E293B !important;
            color: #FFFFFF !important;
        }
        li[role="option"]:hover {
            background-color: #334155 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. KOREKSI STRUKTUR SIDEBAR & FIX DROPDOWN OVERFLOW
# =====================================================================
st.markdown("""
    <style>
    /* Menghentikan pemotongan elemen di area sidebar (Anti-clipping logic) */
    [data-testid="stSidebar"], 
    [data-testid="stSidebarUserContent"],
    .stSelectbox, 
    div[data-baseweb="select"] {
        overflow: visible !important;
    }
    
    /* Memaksa popover daftar dropdown melayang di lapisan teratas screen */
    div[data-baseweb="popover"], div[role="listbox"] {
        z-index: 999999 !important;
    }
    
    /* Sentuhan visual pemisah panel kontrol */
    .control-panel-header {
        font-family: 'Consolas', monospace;
        color: #F59E0B;
        font-weight: bold;
        text-transform: uppercase;
        margin-top: 15px;
        margin-bottom: 5px;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)


# =====================================================================
# 4. SYSTEM HOMEPAGE RENDER (UI/UX OVERVIEW)
# =====================================================================
def render_home_page():
    st.markdown("""
        <style>
        .uawis-header {
            padding: 35px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            margin-bottom: 35px;
        }
        .uawis-header h1 {
            margin: 0;
            font-size: 2.8rem;
            font-family: 'Consolas', monospace;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .status-badge {
            background-color: #059669;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            vertical-align: middle;
            margin-left: 10px;
        }
        .module-card {
            padding: 25px;
            border-radius: 10px;
            border-top: 4px solid #F59E0B;
            text-align: center;
            height: 100%;
            transition: transform 0.2s ease;
        }
        .module-card:hover {
            transform: translateY(-5px);
            border-top: 4px solid #00B4D8;
        }
        .module-card h3 { 
            font-size: 1.4rem; 
            margin-bottom: 15px;
        }
        .module-card p {
            font-size: 0.95rem;
            line-height: 1.5;
            font-family: sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="uawis-header">
            <h1>🌐 U-AWIS COMMAND CENTER</h1>
            <p>Unified Aviation Weather Information System — Sistem Terpadu Pemantauan Meteorologi Penerbangan</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📡 System Modules Status <span class='status-badge'>ONLINE</span>", unsafe_allow_html=True)
    st.write("") 
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="module-card">
            <h3>🛰️ Tactical METAR & TAF</h3>
            <p>Sistem pemantauan cuaca taktis real-time. Menampilkan data observasi (METAR) dan prakiraan (TAF) untuk pangkalan TNI AU di seluruh wilayah Indonesia.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="module-card">
            <h3>📊 Aviation Climatology</h3>
            <p>Sistem rekapitulasi histori cuaca. Menyajikan ringkasan kondisi aerodrome RSN berdasarkan pengolahan data ACS periode 2021 hingga 2025.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="module-card">
            <h3>🌤️ Diurnal Patterns</h3>
            <p>Sistem analisis meteorologi lanjutan. Memetakan pola diurnal aerodrome RSN dari data ACS 2021-2025 untuk mendukung perencanaan penerbangan.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("ℹ️ **Petunjuk Penggunaan:** Silakan buka menu navigasi (Sidebar) di sebelah kiri layar untuk memilih dan menjalankan spesifik modul dashboard.")
    st.caption("U-AWIS Unified Platform © 2026")


# =====================================================================
# 5. REGISTRASI HALAMAN & RUN ROUTER NAVIGASI
# =====================================================================
page_home = st.Page(
    render_home_page, 
    title="U-AWIS Overview", 
    icon="🏠", 
    default=True
)

page_metar = st.Page(
    "metar_dashboard.py", 
    title="Tactical METAR & TAF", 
    icon="🛰️"
)

page_acs = st.Page(
    "acs_dashboard.py", 
    title="Aviation Climatology", 
    icon="📊"
)

page_diurnal = st.Page(
    "meteogram_dashboard.py", 
    title="Diurnal Patterns", 
    icon="🌤️"
)

# Struktur Navigasi Utama Otomatis dinaikkan posisinya di atas Panel Kontrol tambahan
pg = st.navigation({
    "MAIN SYSTEM": [page_home],
    "OPERATIONAL MODULES": [page_metar, page_acs, page_diurnal]
})

# Menjalankan router inti Streamlit
pg.run()
