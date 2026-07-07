import streamlit as st

# =====================================================================
# U-AWIS: MAIN CONTAINER & ROUTER
# Arsitektur: Isolated Page Navigation dengan Injeksi Tema Global via CSS
# =====================================================================

def render_home_page():
    """
    Fungsi untuk merender antarmuka halaman utama U-AWIS.
    Ditempatkan di dalam fungsi agar st.set_page_config tidak bertabrakan
    dengan st.set_page_config yang ada di script dashboard lainnya.
    """
    st.set_page_config(
        page_title="U-AWIS | Unified Aviation Weather",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # =====================================================================
    # INJEKSI CSS GLOBAL (Menggantikan config.toml untuk Tema Sidebar & Konten)
    # =====================================================================
    st.markdown("""
        <style>
        /* Pengaturan Tema Aplikasi Utama (Deep Navy & Slate Gray) */
        .stApp {
            background-color: #0A1128 !important;
            color: #E2E8F0 !important;
            font-family: 'Consolas', 'Roboto Mono', monospace !important;
        }
        
        /* Pengaturan Warna Sidebar Navigasi secara Agresif agar Sinkron */
        [data-testid="stSidebar"] {
            background-color: #162A4A !important;
        }
        [data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
        }
        [data-testid="stSidebarNav"] ul li div:hover {
            background-color: #00B4D822 !important;
        }
        
        /* Komponen Header U-AWIS */
        .uawis-header {
            background: linear-gradient(135deg, #162A4A 0%, #0D1B2A 100%);
            padding: 35px;
            border-radius: 12px;
            border-left: 6px solid #00B4D8;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            margin-bottom: 35px;
        }
        .uawis-header h1 {
            color: #00B4D8 !important;
            margin: 0;
            font-size: 2.8rem;
            font-family: 'Consolas', monospace;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .uawis-header p {
            color: #94A3B8;
            font-size: 1.15rem;
            margin-top: 10px;
            font-family: sans-serif;
        }
        
        /* Status Badge Online */
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
        
        /* Kartu Informasi Modul */
        .module-card {
            background-color: #1E293B;
            padding: 25px;
            border-radius: 10px;
            border-top: 4px solid #F59E0B;
            text-align: center;
            height: 100%;
            transition: transform 0.2s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .module-card:hover {
            transform: translateY(-5px);
            border-top: 4px solid #00B4D8;
        }
        .module-card h3 { 
            color: #F59E0B; 
            font-size: 1.4rem; 
            margin-bottom: 15px;
        }
        .module-card p {
            color: #CBD5E1; 
            font-size: 0.95rem;
            line-height: 1.5;
            font-family: sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

    # ==========================
    # KONTEN UI HALAMAN UTAMA
    # ==========================
    st.markdown("""
        <div class="uawis-header">
            <h1>🌐 U-AWIS COMMAND CENTER</h1>
            <p>Unified Aviation Weather Information System — Sistem Terpadu Pemantauan Meteorologi Penerbangan</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📡 System Modules Status <span class='status-badge'>ONLINE</span>", unsafe_allow_html=True)
    st.write("") # Spacer
    
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
# REGISTRASI HALAMAN & ROUTING (BLACK-BOX ISOLATION)
# =====================================================================

# 1. Halaman Overview (Container Utama)
page_home = st.Page(
    render_home_page, 
    title="U-AWIS Overview", 
    icon="🏠", 
    default=True
)

# 2. Halaman Modul (Memanggil file script asli sebagai modul terisolasi)
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


# =====================================================================
# INISIALISASI NAVIGASI UTAMA
# =====================================================================
try:
    # Mengelompokkan halaman secara seamless di sidebar
    pg = st.navigation({
        "MAIN SYSTEM": [page_home],
        "OPERATIONAL MODULES": [page_metar, page_acs, page_diurnal]
    })
    
    # Jalankan sistem router
    pg.run()
    
except Exception as e:
    st.error("Terjadi kegagalan sistem pada saat memuat modul navigasi.")
    st.code(str(e))
