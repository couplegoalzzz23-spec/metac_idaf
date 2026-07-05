import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 1. GLOBAL MULTI-PAGE GUARD (Mencegah Crash Konfigurasi Modul Terkunci)
# ==============================================================================
if 'original_set_page_config' not in st.__dict__:
    st.original_set_page_config = st.set_page_config
    st.set_page_config = lambda *args, **kwargs: None

# Eksekusi konfigurasi utama secara aman melalui original handler
st.original_set_page_config(
    page_title="Integrated Aviation Weather Center",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS bertema Komando Penerbangan (Navy Blue, Air Force Blue, & Gold)
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
    
    /* Card Panel Styling */
    .command-card {
        background-color: var(--light-gray);
        padding: 24px;
        border-radius: 10px;
        border-left: 6px solid var(--af-blue);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. HALAMAN KUSTOM (CUSTOM PAGES)
# ==============================================================================
def show_home() -> None:
    st.markdown("<h1>🏠 Tactical Meteorological Command Center</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 2px solid #D4AF37; opacity: 0.6;'>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("""
        <div class="command-card">
            <h3>Deskripsi Sistem</h3>
            <p>Sistem Informasi Cuaca Penerbangan Terpadu ini merupakan platform <i>Decision Support System (DSS)</i> tingkat operasional murni. Sistem mengintegrasikan dimensi pemantauan taktis seketika, analisis sinoptik harian, dan perencanaan strategis klimatologi aerodrome ke dalam satu kesatuan arsitektur tanpa mengorbankan logika bisnis inti dari masing-masing sub-sistem.</p>
        </div>
        <div class="command-card">
            <h3>Objektif Utama</h3>
            <ul>
                <li>Menyediakan taklimat cuaca operasional (Operational Weather Briefing) yang cepat dan presisi untuk personel penerbang dan Flight Dispatcher.</li>
                <li>Melakukan otomatisasi pengolahan data klimatologi jangka panjang sesuai standar komputasi WMO dan ICAO Annex 3.</li>
                <li>Meminimalisir kegagalan sistem akibat perbedaan struktur pembacaan berkas eksternal melalui pengamanan lapisan kontainer data.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🗺️ Alur Arsitektur Informasi Sistem")
        st.info("Home System ➔ [📡 Real-Time Hub] ➔ [📈 Analisis Diurnal] ➔ [📊 Probabilitas ACS] ➔ Perencanaan Penerbangan.")

    with col_right:
        st.markdown("### 📊 Ringkasan Statistika Data")
        st.markdown("""
        <div class="metric-box" style="margin-bottom: 12px;">
            <span style="color: #0B3C5D; font-weight:600; font-size:0.9rem;">PERIODE OBSERVASI</span>
            <h2 style="margin:5px 0; color:#328CC1 !important;">5 Tahun</h2>
            <span style="color: #777; font-size:0.8rem;">Rentang Data: 2021 - 2025</span>
        </div>
        <div class="metric-box" style="margin-bottom: 12px;">
            <span style="color: #0B3C5D; font-weight:600; font-size:0.9rem;">TOTAL PARAMETER INTI</span>
            <h2 style="margin:5px 0; color:#328CC1 !important;">5 Komponen</h2>
            <span style="color: #777; font-size:0.8rem;">Temp, RH, Vis, Cloud, Wind</span>
        </div>
        <div class="metric-box">
            <span style="color: #0B3C5D; font-weight:600; font-size:0.9rem;">BERKAS DATASET TERVERIFIKASI</span>
            <h2 style="margin:5px 0; color:#328CC1 !important;">6 Spreadsheet</h2>
            <span style="color: #777; font-size:0.8rem;">Format: Microsoft Excel (.xlsx)</span>
        </div>
        """, unsafe_allow_html=True)

def show_briefing() -> None:
    st.markdown("<h1>✈️ Aviation Weather Briefing Center</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 2px solid #D4AF37; opacity: 0.6;'>", unsafe_allow_html=True)
    
    st.markdown("### Sintesis Multi-Dimensi Data Cuaca & Analisis Dampak Operasional")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="command-card" style="border-left-color: #E74C3C;">
            <h4>📡 1. KONDISI TENTATIF (Taktis)</h4>
            <p><b>Observation METAR:</b><br><code style="color:#E74C3C;">4000 BR BKN012</code></p>
            <p>Jarak pandang mendatar mengalami penurunan akibat terbentuknya partikel mist/kondensasi basah permukaan rendah.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="command-card" style="border-left-color: #F1C40F;">
            <h4>📈 2. POLA DIURNAL (Sinoptik)</h4>
            <p><b>Kecenderungan Harian:</b><br>Berdasarkan grafik harian, penurunan visibility ke level ekstrim terendah dominan terkonsentrasi pada pukul 22.00 - 00.00 UTC (05.00 - 07.00 WIB).</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="command-card" style="border-left-color: #2ECC71;">
            <h4>📊 3. FREKUENSI KLIMATOLOGI (ACS)</h4>
            <p><b>Probabilitas Historis:</b><br>Frekuensi kumulatif spasial untuk kejadian Jarak Pandang (Visibility) &lt; 5000 meter pada bulan berjalan secara statistik adalah <b>28%</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 🎯 Implikasi Operasional & Rekomendasi Taktis")
    st.error("⚠️ **POTENSI KETERLAMBATAN PENDEKATAN IFR (IFR APPROACH DELAY):** Diimbau kepada seluruh ATC dan operator penerbangan untuk memperhitungkan tambahan cadangan bahan bakar penahanan (*holding fuel*) serta memastikan kesiapan *alternate aerodrome* terdekat yang memiliki instrumen pendaratan presisi.")

def show_metadata() -> None:
    st.markdown("<h1>📄 Validasi Dokumen & Manajemen Metadata</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 2px solid #D4AF37; opacity: 0.6;'>", unsafe_allow_html=True)
    
    base_dir = Path(__file__).parent
    target_files = [
        "rekap_hs_2021_2025.xlsx",
        "rekap_rh_max_min_2021_2025.xlsx",
        "rekap_temp_max_min_2021_2025.xlsx",
        "rekap_temperature_2021_2025.xlsx",
        "rekap_visibility_2021_2025.xlsx",
        "rekap_wind_2021_2025.xlsx"
    ]
    
    meta_records = []
    for f_name in target_files:
        f_path = base_dir / f_name
        if f_path.exists():
            f_stat = f_path.stat()
            size_mb = f_stat.st_size / (1024 * 1024)
            mod_date = datetime.fromtimestamp(f_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            try:
                excel_obj = pd.ExcelFile(f_path, engine='openpyxl')
                sheet_names = excel_obj.sheet_names
                sample_df = pd.read_excel(f_path, sheet_name=sheet_names[0], engine='openpyxl')
                rows, cols = sample_df.shape
                missing_vals = sample_df.isnull().sum().sum()
                status = "✅ Validated"
            except Exception:
                sheet_names, rows, cols, missing_vals = [], 0, 0, 0
                status = "❌ Corrupted"
                
            meta_records.append({
                "Nama Berkas": f_name,
                "Ukuran (MB)": f"{size_mb:.2f}",
                "Jumlah Sheet": len(sheet_names),
                "Dimensi Data (Row x Col)": f"{rows} x {cols}",
                "Missing Values": missing_vals,
                "Status Integritas": status,
                "Pembaruan Server": mod_date
            })
        else:
            meta_records.append({
                "Nama Berkas": f_name, "Ukuran (MB)": "N/A", "Jumlah Sheet": 0,
                "Dimensi Data (Row x Col)": "N/A", "Missing Values": "N/A",
                "Status Integritas": "⚠️ Missing File", "Pembaruan Server": "N/A"
            })
            
    st.dataframe(pd.DataFrame(meta_records), use_container_width=True, hide_index=True)

def show_about() -> None:
    st.markdown("<h1>ℹ️ Mengenai Aplikasi</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 2px solid #D4AF37; opacity: 0.6;'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="command-card">
        <h4>Standar Operasional & Kepatuhan Perangkat Lunak</h4>
        <p>Aplikasi ini dirancang sebagai purwarupa sistem manajemen informasi cuaca militer yang patuh pada regulasi internasional <b>WMO (World Meteorological Organization) No. 49</b> dan <b>ICAO Annex 3</b>.</p>
        <p><b>Arsitektur:</b> Clean Multi-Page Isolation Node<br>
        <b>Penyusun:</b> Tim Ahli Pengembang Perangkat Lunak & Sistem Informasi Meteorologi Penerbangan.</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. HIGH-LEVEL NAVIGATION ROUTER (Streamlit 1.35+ Engine)
# ==============================================================================
# Inisialisasi peta halaman menggunakan komponen native st.Page
page_home = st.Page(show_home, title="Home", icon="🏠", default=True)
page_metar = st.Page("metar_dashboard.py", title="Real-Time Weather", icon="📡")
page_diurnal = st.Page("meteogram_dashboard.py", title="Diurnal Meteogram", icon="📈")
page_acs = st.Page("acs_dashboard.py", title="ACS Climatology", icon="📊")
page_briefing = st.Page(show_briefing, title="Aviation Weather Briefing", icon="✈️")
page_metadata = st.Page(show_metadata, title="Metadata", icon="📄")
page_about = st.Page(show_about, title="About Dashboard", icon="ℹ️")

# Build navigasi terisolasi
selected_page = st.navigation({
    "MAIN COMMAND": [page_home],
    "METEOROLOGICAL CORE": [page_metar, page_diurnal, page_acs],
    "TACTICAL ANALYSIS": [page_briefing, page_metadata, page_about]
})

# Eksekusi halaman terpilih tanpa bentrokan variabel global
selected_page.run()
