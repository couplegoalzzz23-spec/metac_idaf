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

# Konfigurasi Utama Command Center (Aviation Center Theme)
st.original_set_page_config(
    page_title="Integrated Aviation Weather Center",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 1.5 PRESENTATION LAYER (Global CSS Injection - Tactical Dark Mode)
# Mengunci visual premium tanpa merusak struktur dan logika script asli
# ==============================================================================
st.markdown("""
    <style>
    /* Premium Font Integration */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Memaksa Tampilan Elemen Utama ke Spektrum Dark Mode Kontras Tinggi */
    .stApp, .stApp > header {
        background-color: #0B0F19 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #060913 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    [data-testid="stSidebarNav"] {
        background-color: #060913 !important;
    }

    /* Pembenahan Tipografi & Judul */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    p, span, label, .stMarkdown {
        color: #94A3B8 !important;
    }

    /* Kotak Informasi & Kartu Bergaya Command Center */
    .command-card {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 20px !important;
    }
    
    .command-card h3 {
        color: #10B981 !important; /* Hijau Taktis Penerbangan */
        margin-top: 0px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .command-card p {
        color: #E2E8F0 !important;
        line-height: 1.6 !important;
    }

    /* Efek Hover Dinamis di Menu Samping */
    [data-testid="stSidebarNav"] ul li div {
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    [data-testid="stSidebarNav"] ul li div:hover {
        background-color: rgba(16, 185, 129, 0.1) !important;
    }
    
    /* Mengubah Gaya Notifikasi Sukses */
    div.stAlert {
        background-color: #064E3B !important;
        color: #A7F3D0 !important;
        border: 1px solid #10B981 !important;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. HALAMAN BERANDA (PRESENTATION LAYER ONLY)
# ==============================================================================
def show_home():
    st.markdown("""
    <div class="command-card">
        <h3>⚡ SYSTEM INTEGRATION SECURITY: STATUS ACTIVE</h3>
        <p>Sistem ini telah berhasil diintegrasikan menggunakan arsitektur <b>Multi-Page Isolated Node</b> tingkat produksi. 
        Modul Taktis (METAR), Sinoptik (Meteogram), dan Klimatologi (ACS) kini beroperasi secara independen dan aman di dalam satu super-framework tanpa risiko tabrakan antarmuka (UI).</p>
        <p>Silakan gunakan panel navigasi di sebelah kiri untuk beralih antar subsistem cuaca.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Engine Status: ONLINE. Sistem beroperasi stabil pada arsitektur Streamlit Cloud.")


# ==============================================================================
# 3. SISTEM ROUTING MODERN (Streamlit >= 1.35)
# KUNCI TOTAL: Struktur Pemanggilan Target Dashboard 100% Sama dengan Kode Asli
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

# Jalankan Router
nav.run()
