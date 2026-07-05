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

# Custom CSS - Tema Komando Penerbangan TNI AU
st.markdown("""
    <style>
    :root {
        --navy-blue: #0B3C5D;
        --af-blue: #328CC1;
        --gold: #D4AF37;
        --light-gray: #F0F2F6;
        --white: #FFFFFF;
    }
    .stApp { background-color: var(--white); }
    h1, h2, h3 { color: var(--navy-blue) !important; font-weight: 700; font-family: 'Helvetica Neue', sans-serif;}
    
    .command-card {
        background-color: var(--light-gray);
        padding: 24px;
        border-radius: 10px;
        border-left: 6px solid var(--af-blue);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    hr { border-top: 2px solid var(--gold); opacity: 0.6; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DEFINISI HALAMAN KUSTOM
# ==============================================================================
def show_home():
    st.markdown("<h1>🏠 Tactical Meteorological Command Center</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="command-card">
        <h3>Selamat Datang di Sistem Informasi Cuaca Terpadu</h3>
        <p>Sistem ini telah berhasil diintegrasikan menggunakan arsitektur <b>Multi-Page Isolated Node</b> tingkat produksi. 
        Modul Taktis (METAR), Sinoptik (Meteogram), dan Klimatologi (ACS) kini beroperasi secara independen dan aman di dalam satu super-framework tanpa risiko tabrakan antarmuka (UI).</p>
        <p>Silakan gunakan panel navigasi di sebelah kiri untuk beralih antar subsistem cuaca.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Engine Status: ONLINE. Sistem beroperasi stabil pada arsitektur Streamlit Cloud.")

# ==============================================================================
# 3. SISTEM ROUTING MODERN (Streamlit >= 1.35)
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
