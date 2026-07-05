import streamlit as st
import pandas as pd
import os
from pathlib import Path
import runpy
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & MILITARY UI THEME
# ==========================================
st.set_page_config(
    page_title="Integrated Aviation Weather Center",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TNI AU Inspired Theme CSS
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
    h1, h2, h3 { color: var(--navy-blue); font-weight: 700; font-family: 'Helvetica Neue', sans-serif;}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--navy-blue);
        color: var(--white);
        border-right: 2px solid var(--gold);
    }
    .st-emotion-cache-16txtl3 h1, .st-emotion-cache-16txtl3 h2, .st-emotion-cache-16txtl3 h3, .st-emotion-cache-16txtl3 p {
        color: var(--white) !important;
    }
    
    /* Cards and Metrics */
    div[data-testid="stMetricValue"] { color: var(--af-blue); font-size: 1.8rem; font-weight: bold;}
    div[data-testid="stMetricLabel"] { color: var(--navy-blue); font-weight: 600;}
    
    .card-panel {
        background-color: var(--light-gray);
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid var(--af-blue);
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Divider */
    hr { border-top: 2px solid var(--gold); opacity: 0.5; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE SYSTEM: SAFE MODULE LOADER
# ==========================================
def execute_locked_module(filename):
    """
    Menjalankan legacy script tanpa memodifikasi kodenya.
    Mencegah bentrokan st.set_page_config() dengan monkeypatching sementara.
    """
    file_path = Path(__file__).parent / filename
    if not file_path.exists():
        st.error(f"🚨 **SYSTEM FAILURE:** Modul terpisah `{filename}` tidak ditemukan di direktori sistem.")
        st.info("Pastikan file modul legacy telah diunggah sesuai dengan nama yang dibutuhkan.")
        return

    # Back-up Streamlit config function
    original_set_page_config = st.set_page_config
    # Override untuk menetralisir panggilan config dari child module
    st.set_page_config = lambda *args, **kwargs: None
    
    try:
        runpy.run_path(str(file_path), run_name="__main__")
    except Exception as e:
        st.error(f"🚨 **RUNTIME EXCEPTION:** Gagal mengeksekusi algoritma pada `{filename}`.")
        st.code(str(e))
    finally:
        # Kembalikan ke fungsi normal
        st.set_page_config = original_set_page_config

# ==========================================
# 3. DASHBOARD VIEWS (NEW MODULES)
# ==========================================
def render_home():
    st.markdown("<h1>🏠 Tactical Meteorological Command Center</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="card-panel">
            <h3>Tujuan Sistem Operasional</h3>
            <p>Integrated Aviation Weather Dashboard dirancang sebagai <i>Decision Support System</i> tingkat lanjut untuk operasional penerbangan TNI AU dan instansi sipil. 
            Sistem ini memadukan tiga dimensi kesadaran cuaca:</p>
            <ul>
                <li><b>Real-Time (Tactical):</b> "Apa yang terjadi sekarang?"</li>
                <li><b>Diurnal (Synoptic):</b> "Bagaimana pola cuaca sepanjang hari?"</li>
                <li><b>ACS Climatology (Strategic):</b> "Seberapa sering suatu kejadian cuaca ekstrem terjadi?"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("### Quick Statistics")
        st.metric(label="Total Observation Years", value="5 Years", delta="2021-2025", delta_color="off")
        st.metric(label="Integrated Core Modules", value="3 Systems", delta="Realtime, Diurnal, ACS")
        
    st.markdown("### 🗂️ System Architecture Diagram")
    st.info("Sistem ini dibangun dengan arsitektur Modular Tersilokasi, memungkinkan modul lawas beroperasi di dalam super-framework tanpa mengubah integritas data WMO (World Meteorological Organization).")

def render_briefing():
    st.markdown("<h1>✈️ Aviation Weather Briefing (Cross-Analysis)</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("*Modul ini mensintesis data terkini dengan pola historis untuk mitigasi risiko taktis.*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📡 1. TACTICAL (Current)")
        st.warning("**Kondisi Simulasi:**\nVisibility: 4000m\nWeather: BR (Mist)\nCloud: BKN012")
    with col2:
        st.markdown("### 📈 2. SYNOPTIC (Diurnal)")
        st.info("**Pola Harian:**\nPenurunan jarak pandang terendah secara statistik terjadi pada pukul 22.00 - 01.00 UTC (05.00 - 08.00 LT).")
    with col3:
        st.markdown("### 📊 3. STRATEGIC (ACS)")
        st.error("**Probabilitas Historis:**\nProbabilitas kejadian visibility di bawah 5000m pada bulan saat ini adalah **28%**.")

    st.markdown("---")
    st.markdown("### 🎯 Operational Implication (Decision Support)")
    st.success("Terdapat potensi perlambatan operasi darat dan pendekatan (IFR approach delay). Direkomendasikan untuk menyiapkan *alternate aerodrome* dan memperhitungkan tambahan cadangan *holding fuel*.")

def render_metadata():
    st.markdown("<h1>📄 Sistem Manajemen Metadata WMO</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    data_dir = Path(__file__).parent
    excel_files = list(data_dir.glob("*.xlsx"))
    
    if not excel_files:
        st.warning("Tidak ada dataset observasi berekstensi .xlsx yang terdeteksi di server.")
        return
        
    metadata = []
    for file in excel_files:
        try:
            stat = file.stat()
            size_mb = stat.st_size / (1024 * 1024)
            mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # Cek struktur ringan
            xls = pd.ExcelFile(file, engine='openpyxl')
            sheets = len(xls.sheet_names)
            
            metadata.append({
                "Nama Dokumen": file.name,
                "Ukuran (MB)": f"{size_mb:.2f}",
                "Jumlah Sheet": sheets,
                "Status Validasi": "✅ Verified",
                "Terakhir Dimodifikasi": mod_time
            })
        except Exception as e:
            metadata.append({
                "Nama Dokumen": file.name,
                "Ukuran (MB)": "ERROR",
                "Jumlah Sheet": "ERROR",
                "Status Validasi": "❌ Corrupt",
                "Terakhir Dimodifikasi": "N/A"
            })
            
    df_meta = pd.DataFrame(metadata)
    st.dataframe(df_meta, use_container_width=True, hide_index=True)

def render_about():
    st.markdown("<h1>ℹ️ About Tactical Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    Sistem Informasi Cuaca Penerbangan Terpadu ini dikembangkan secara spesifik untuk memenuhi standar keandalan perangkat lunak militer dan penerbangan tingkat tinggi.
    
    **Development Core:**
    * **Standard:** ICAO Annex 3 & WMO Guidelines
    * **Framework:** Streamlit (Python 3.11)
    * **Architecture:** Fault-Tolerant Modular Enclosure
    * **Maintainability:** Dirancang dengan konsep *Locked Modules* sehingga update di masa depan pada algoritma kalkulasi tidak merusak antarmuka utama.
    
    *Dikembangkan secara komprehensif oleh Tim Multidisiplin Ahli IT & Meteorologi.*
    """)

# ==========================================
# 4. MAIN ROUTER & SIDEBAR NAVIGATION
# ==========================================
def main():
    st.sidebar.markdown("## 🧭 COMMAND CENTER")
    st.sidebar.caption("Tactical & Synoptic Systems")
    
    # Hierarki Navigasi
    pages = {
        "🏠 Home": render_home,
        "📡 Real-Time Weather": lambda: execute_locked_module("metar_dashboard.py"),
        "📈 Diurnal Meteogram": lambda: execute_locked_module("meteogram_dashboard.py"),
        "📊 ACS Climatology": lambda: execute_locked_module("acs_dashboard.py"),
        "✈️ Aviation Weather Briefing": render_briefing,
        "🔍 Cross Analysis": lambda: st.info("Modul Cross Analysis sedang dalam antrean integrasi big data BMKG."),
        "📄 Metadata": render_metadata,
        "ℹ️ About Dashboard": render_about
    }
    
    selection = st.sidebar.radio("Sistem Navigasi Utama:", list(pages.keys()))
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='font-size: 0.8rem; text-align: center; color: #D4AF37;'>
    <b>STATUS:</b> ONLINE<br>
    <b>SECURE CONNECTION</b>
    </div>
    """, unsafe_allow_html=True)
    
    # Eksekusi halaman yang dipilih
    pages[selection]()

if __name__ == "__main__":
    main()
