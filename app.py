import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from fpdf import FPDF
from datetime import datetime, timezone
import re
from bs4 import BeautifulSoup

# ==========================================
# 0. GLOBAL PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="TNI AU Integrated Aviation & Tactical Weather Portal",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. ENTERPRISE PRESENTATION LAYER (CSS DESIGN SYSTEM)
# ==========================================
def load_css():
    st.markdown("""
    <style>
    /* Global Background & Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    code, pre, .stCode {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Dark Mode Theme Enforcement */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        background-image: radial-gradient(rgba(56, 189, 248, 0.05) 1px, transparent 0);
        background-size: 24px 24px;
    }
    
    /* Typography Hierarchy */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    p, span, label {
        color: #CBD5E1;
    }
    
    /* Hero Section Glassmorphism Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid #38BDF8;
        border-radius: 18px;
        padding: 24px 32px;
        margin-bottom: 28px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(12px);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    
    .hero-title {
        font-size: 26px;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .hero-subtitle {
        font-size: 14px;
        color: #94A3B8;
        margin-top: 4px;
    }
    
    .status-badge {
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid #22C55E;
        color: #22C55E;
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 0.5px;
    }
    
    .status-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background-color: #22C55E;
        border-radius: 50%;
        box-shadow: 0 0 8px #22C55E;
    }
    
    /* Premium Card & Metric Container Styling */
    div[data-testid="metric-container"] {
        background: #1E293B;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 12px 32px rgba(56, 189, 248, 0.15);
    }
    
    div[data-testid="metric-container"]::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #38BDF8, transparent);
    }
    
    div[data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-weight: 700 !important;
        font-size: 28px !important;
        font-family: 'JetBrains Mono', monospace;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #CBD5E1 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Floating Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* Interactive Buttons & Tabs */
    .stButton > button {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.25s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        background: #38BDF8;
        color: #0F172A;
        border-color: #38BDF8;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #111827;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #CBD5E1;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Radar Animation for Tactical Ops */
    .radar {
        position: relative;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(56,189,248,0.05) 20%, transparent 21%),
                    radial-gradient(circle, rgba(56,189,248,0.1) 10%, transparent 11%);
        background-size: 20px 20px;
        border: 2px solid #38BDF8;
        overflow: hidden;
        margin: 15px auto;
        box-shadow: 0 0 25px rgba(56,189,248,0.25);
    }
    
    .radar:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 50%;
        height: 2px;
        background: linear-gradient(90deg, #38BDF8, transparent);
        transform-origin: 100% 50%;
        animation: sweep 2.5s linear infinite;
    }
    
    @keyframes sweep {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Expanders & Dataframes */
    .st-expander {
        background-color: #1E293B !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
    }
    
    hr, .stDivider {
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==========================================
# CONSTANTS & METEOROLOGICAL DICTIONARIES
# ==========================================
BAKU_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
MONTHS_ID = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

LANUD_MAP = {
    "Lanud Halim Perdanakusuma (WIHH)": ["WIHH", "WIII"],
    "Lanud Atang Sendjaja (WIAJ)": ["WIAJ", "WIHH", "WIII"],
    "Lanud Suryadarma (WIAK)": ["WIAK", "WICC", "WIIH"],
    "Lanud Husein Sastranegara (WICC)": ["WICC", "WIII"],
    "Lanud Sugiri Sukani (WIER)": ["WIER", "WICN", "WICC"],
    "Lanud Sutan Sjahrir - Padang (WIMG)": ["WIMG", "WIEE"], 
    "Lanud Soewondo - Medan (WIMK)": ["WIMK", "WIMM"],     
    "Lanud Roesmin Nurjadin (WIBB)": ["WIBB"],
    "Lanud Supadio (WIOO)": ["WIOO"],
    "Lanud Sultan Iskandar Muda (WITT)": ["WITT"],
    "Lanud Sri Mulyono Herlambang (WIPP)": ["WIPP"],
    "Lanud Radin Inten II (WILL)": ["WILL"],
    "Lanud Raja Haji Fisabilillah (WIDN)": ["WIDN"],
    "Lanud Hang Nadim (WIDD)": ["WIDD"],
    "Lanud Raden Sadjad (WION)": ["WION"],
    "Lanud Iswahjudi (WARI)": ["WARI", "WARQ", "WARR"], 
    "Lanud Abdulrachman Saleh (WARA)": ["WARA", "WARR"], 
    "Lanud Adisutjipto (WARJ)": ["WARJ", "WAHH", "WARQ"], 
    "Lanud Juanda (WARR)": ["WARR"],
    "Lanud Sultan Hasanuddin (WAAA)": ["WAAA"],
    "Lanud I Gusti Ngurah Rai (WADD)": ["WADD"],
    "Lanud El Tari (WATT)": ["WATT"],
    "Lanud Sam Ratulangi (WAMM)": ["WAMM"],
    "Lanud Syamsudin Noor (WAOO)": ["WAOO"],
    "Lanud Dhomber (WALL)": ["WALL"],
    "Lanud Iskandar (WAOI)": ["WAOI"],
    "Lanud Silas Papare (WAJJ)": ["WAJJ"],
    "Lanud Manuhua (WABB)": ["WABB"],
    "Lanud Johanes Kapiyau (WABI)": ["WABI"],
    "Lanud Pattimura (WAPP)": ["WAPP"],
    "Lanud Leo Wattimena (WAMW)": ["WAMW"],
    "Lanud J.A. Dimara (WAKK)": ["WAKK"],
}

PROVINCE_ADM1_MAP = {
    "Aceh (11)": "11", "Sumatera Utara (12)": "12", "Sumatera Barat (13)": "13", 
    "Riau (14)": "14", "Jambi (15)": "15", "Sumatera Selatan (16)": "16", 
    "Bengkulu (17)": "17", "Lampung (18)": "18", "Kepulauan Bangka Belitung (19)": "19", 
    "Kepulauan Riau (21)": "21", "DKI Jakarta (31)": "31", "Jawa Barat (32)": "32", 
    "Jawa Tengah (33)": "33", "DI Yogyakarta (34)": "34", "Jawa Timur (35)": "35", 
    "Banten (36)": "36", "Bali (51)": "51", "Nusa Tenggara Barat (52)": "52", 
    "Nusa Tenggara Timur (53)": "53", "Kalimantan Barat (61)": "61", 
    "Kalimantan Tengah (62)": "62", "Kalimantan Selatan (63)": "63", 
    "Kalimantan Timur (64)": "64", "Kalimantan Utara (65)": "65", 
    "Sulawesi Utara (71)": "71", "Sulawesi Tengah (72)": "72", 
    "Sulawesi Selatan (73)": "73", "Sulawesi Tenggara (74)": "74", 
    "Gorontalo (75)": "75", "Sulawesi Barat (76)": "76", "Maluku (81)": "81", 
    "Maluku Utara (82)": "82", "Papua (91)": "91", "Papua Barat (92)": "92",
    "Papua Selatan (93)": "93", "Papua Tengah (94)": "94", 
    "Papua Pegunungan (95)": "95", "Papua Barat Daya (96)": "96"
}

API_BASE = "https://cuaca.bmkg.go.id/api/df/v1/forecast/adm"
MS_TO_KT = 1.94384
METAR_API = "https://aviationweather.gov/api/data/metar"
SATELLITE_HIMA_RIAU = "http://202.90.198.22/IMAGE/HIMA/H08_RP_Riau.png"

# ==========================================
# MODULE 1 FUNCTIONS: ACS CLIMATOLOGY ENGINE
# ==========================================
@st.cache_data(show_spinner=False)
def load_data(filename):
    filepath = filename if os.path.exists(filename) else os.path.join("data", filename)
    if not os.path.exists(filepath):
        st.error(f"🚨 File tidak ditemukan: `{filename}`. Pastikan nama file sesuai di repositori.")
        return None
    try:
        raw_df = pd.read_excel(filepath, header=None)
        header_idx = 0
        for i in range(min(15, len(raw_df))):
            row_vals = [str(x).upper().strip() for x in raw_df.iloc[i].fillna('')]
            if any(c in row_vals for c in ['DATE', 'BULAN', 'MONTH', 'JAN', 'JANUARI', 'JANUARY']):
                if 'JAN' in row_vals or 'JANUARI' in row_vals or 'JANUARY' in row_vals:
                    header_idx = max(0, i - 1)
                else:
                    header_idx = i
                break
        df = raw_df.iloc[header_idx+1:].copy()
        df.columns = raw_df.iloc[header_idx].astype(str).str.strip()
        df = df.loc[:, df.columns.notna()]
        df = df.loc[:, ~df.columns.str.lower().str.contains('nan|unnamed')]
        date_col = None
        for col in df.columns:
            if str(col).upper() in ['DATE', 'BULAN', 'MONTH']:
                date_col = col
                break
        if date_col:
            df = df.rename(columns={date_col: 'DATE'})
        else:
            df = df.rename(columns={df.columns[0]: 'DATE'})
        valid_months_map = {
            'JAN': 'Jan', 'FEB': 'Feb', 'MAR': 'Mar', 'APR': 'Apr', 'MAY': 'Mei', 'MEI': 'Mei',
            'JUN': 'Jun', 'JUL': 'Jul', 'AUG': 'Agu', 'AGU': 'Agu', 'SEP': 'Sep', 'OCT': 'Okt',
            'OKT': 'Okt', 'NOV': 'Nov', 'DEC': 'Des', 'DES': 'Des'
        }
        df['TEMP_DATE'] = df['DATE'].astype(str).str.upper().str.strip().str[:3]
        df = df[df['TEMP_DATE'].isin(valid_months_map.keys())].copy()
        df = df.drop_duplicates(subset=['TEMP_DATE'], keep='first')
        df['DATE'] = df['TEMP_DATE'].map(valid_months_map)
        df = df.drop(columns=['TEMP_DATE'])
        df['DATE_CAT'] = pd.Categorical(df['DATE'], categories=BAKU_MONTHS, ordered=True)
        df = df.sort_values('DATE_CAT').drop(columns=['DATE_CAT']).reset_index(drop=True)
        for col in df.columns:
            if col == 'DATE': continue
            elif str(col).upper() == 'DIRECTION': df[col] = df[col].astype(str) 
            else: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"🚨 Gagal memproses file {filename}: {str(e)}")
        return None

def get_aviation_notes(parameter):
    notes = {
        "Temperature Freq": "Suhu tinggi berkaitan dengan peningkatan density altitude. Ini menurunkan performa daya angkat pesawat, menuntut take-off roll lebih panjang, dan membatasi Maximum Take-off Weight (MTOW).",
        "Temperature Mean": "Pemahaman fluktuasi rata-rata suhu harian sangat vital bagi flight dispatcher untuk kalkulasi fuel burn dan manajemen beban muatan yang efisien.",
        "Relative Humidity": "RH tinggi (mendekati 100%) mendukung probabilitas pembentukan embun, kabut radiasi, atau low clouds saat terjadi pendinginan nokturnal, berdampak langsung pada jarak pandang.",
        "Visibility": "Visibility rendah meningkatkan potensi gangguan operasi approach dan landing, seringkali memaksa pemberlakuan prosedur IFR (Instrument Flight Rules) dan Low Visibility Procedures (LVP).",
        "Cloud Base": "Cloud base (ceiling) yang sangat rendah berisiko melanggar standar Decision Height (DH). Hal ini meningkatkan peluang missed approach atau pengalihan rute (divert) ke bandara alternatif.",
        "Wind": "Distribusi dominan arah dan kecepatan angin menjadi referensi mutlak evaluasi konfigurasi runway-in-use. Kecepatan angin tinggi memicu windshear/crosswind yang membahayakan fase final approach."
    }
    return notes.get(parameter, "Catatan operasional tidak tersedia.")

def generate_auto_interpretation(df, plot_cols, param_name):
    st.subheader("💡 Interpretasi Karakter Klimatologi")
    st.markdown("Berdasarkan hasil analisis data secara otomatis:")
    if len(plot_cols) == 0:
        st.write("- Tidak cukup data untuk diinterpretasikan.")
        return
    for col in plot_cols[:3]: 
        max_val = df[col].max()
        if max_val > 0:
            max_month_series = df.loc[df[col] == max_val, 'DATE'].values
            max_month = max_month_series[0] if len(max_month_series) > 0 else "N/A"
            st.write(f"- Peluang frekuensi/intensitas tertinggi untuk kondisi **{col}** terjadi pada bulan **{max_month}** (Nilai tertinggi: {max_val}).")

def render_generic_page(title, filename, param_key, chart_type='bar', colorscale="Blues", legend_title="Kategori"):
    st.title(f"{title}")
    st.markdown(f"*{get_aviation_notes(param_key)}*")
    st.markdown("---")
    df = load_data(filename)
    if df is not None and not df.empty:
        plot_cols = [c for c in df.columns if str(c).upper() not in ['DATE', 'DIRECTION']]
        col_chart, col_metric = st.columns([3, 1])
        safe_colorscale = getattr(px.colors.sequential, colorscale, px.colors.sequential.Blues)
        with col_chart:
            st.markdown("### 📈 Interactive Meteogram")
            if chart_type == 'bar':
                fig = px.bar(
                    df, x='DATE', y=plot_cols, barmode='group', 
                    color_discrete_sequence=safe_colorscale,
                    labels={"variable": legend_title, "value": "Nilai / Frekuensi", "DATE": "Bulan"}
                )
            else: 
                fig = go.Figure()
                safe_qualitative = getattr(px.colors.qualitative, 'Plotly', ['#38BDF8', '#EF4444', '#22C55E', '#FACC15'])
                for idx, col in enumerate(plot_cols):
                    fig.add_trace(go.Scatter(
                        x=df['DATE'], y=df[col], mode='lines+markers', 
                        name=str(col), line=dict(width=3, color=safe_qualitative[idx % len(safe_qualitative)])
                    ))
            fig.update_layout(
                xaxis_title="Bulan", yaxis_title="Frekuensi / Nilai", 
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1"), hovermode="x unified", legend_title_text=legend_title
            )
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.08)')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.08)')
            st.plotly_chart(fig, use_container_width=True)

        with col_metric:
            st.markdown("### 🌡️ Heatmap Profil")
            df_heat = df.set_index('DATE')[plot_cols].T
            fig_heat = px.imshow(
                df_heat, text_auto=".1f", aspect="auto", 
                color_continuous_scale=safe_colorscale,
                labels={"x": "Bulan", "y": legend_title, "color": "Nilai"}
            )
            fig_heat.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"), margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_heat, use_container_width=True)
            
        st.markdown("---")
        col_insight, col_data = st.columns([1, 1])
        with col_insight:
            generate_auto_interpretation(df, plot_cols, title)
            st.success("✅ **Operational Note:** " + get_aviation_notes(param_key))
        with col_data:
            st.markdown("### 🗃️ Original Data Table")
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="⬇️ Download CSV", data=csv, file_name=f"{filename.replace('.xlsx', '')}.csv", mime="text/csv", use_container_width=True)
    else:
        st.warning("⚠️ Data kosong atau gagal diolah.")

def render_wind_page():
    st.title("🌬️ Wind Analysis (Arah & Kecepatan)")
    st.markdown(f"*{get_aviation_notes('Wind')}*")
    st.markdown("---")
    df = load_data("rekap_wind_2021_2025.xlsx")
    if df is not None and not df.empty:
        dir_cols = [c for c in df.columns if '-' in str(c) and len(str(c).split('-')) == 3]
        speed_cols = [c for c in df.columns if c not in dir_cols and str(c).upper() not in ['DATE', 'CALM', 'DIRECTION']]
        st.markdown("### 📈 Unified Interactive Windrose & Speed Distribution")
        fig_wind = make_subplots(
            rows=1, cols=2, specs=[[{'type': 'polar'}, {'type': 'xy'}]],
            subplot_titles=("Windrose (Distribusi Arah)", "Distribusi Kecepatan Angin (Bulan)"),
            horizontal_spacing=0.15
        )
        if dir_cols:
            avg_dir = df[dir_cols].mean().reset_index()
            avg_dir.columns = ['Arah', 'Frekuensi']
            fig_wind.add_trace(
                go.Barpolar(
                    r=avg_dir['Frekuensi'], theta=avg_dir['Arah'],
                    marker_color=avg_dir['Frekuensi'], marker_colorscale='Turbo', name="Arah Angin (Avg)", showlegend=False
                ), row=1, col=1
            )
        if speed_cols:
            safe_colorscale = getattr(px.colors.sequential, "Turbo", px.colors.sequential.Viridis)
            colors = px.colors.sample_colorscale(safe_colorscale, [i/(len(speed_cols)-1) if len(speed_cols)>1 else 1 for i in range(len(speed_cols))])
            for idx, col in enumerate(speed_cols):
                fig_wind.add_trace(go.Bar(x=df['DATE'], y=df[col], name=f"{col} Kts", marker_color=colors[idx]), row=1, col=2)
        fig_wind.update_layout(
            barmode='group', polar=dict(radialaxis=dict(visible=True, showticklabels=True), angularaxis=dict(direction="clockwise")),
            legend_title_text="Kategori Kecepatan", height=500, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1")
        )
        fig_wind.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.08)', row=1, col=2)
        fig_wind.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.08)', title_text="Frekuensi", row=1, col=2)
        st.plotly_chart(fig_wind, use_container_width=True)

        st.markdown("### 🌡️ Heatmap Profil Angin")
        col_heat1, col_heat2 = st.columns(2)
        with col_heat1:
            if dir_cols:
                st.markdown("**Distribusi Arah Angin**")
                df_heat_dir = df.set_index('DATE')[dir_cols].T
                fig_hd = px.imshow(df_heat_dir, text_auto=".1f", aspect="auto", color_continuous_scale="Turbo", labels={"x": "Bulan", "y": "Arah", "color": "Frekuensi"})
                fig_hd.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
                st.plotly_chart(fig_hd, use_container_width=True)
        with col_heat2:
            if speed_cols:
                st.markdown("**Distribusi Kecepatan Angin**")
                df_heat_speed = df.set_index('DATE')[speed_cols].T
                fig_hs = px.imshow(df_heat_speed, text_auto=".1f", aspect="auto", color_continuous_scale="Turbo", labels={"x": "Bulan", "y": "Kecepatan (Kts)", "color": "Frekuensi"})
                fig_hs.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
                st.plotly_chart(fig_hs, use_container_width=True)
        st.markdown("---")
        col_insight, col_data = st.columns([1, 1])
        with col_insight:
            st.success("✅ **Operational Note:** " + get_aviation_notes('Wind'))
        with col_data:
            st.markdown("### 🗃️ Original Data Table")
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="⬇️ Download CSV", data=csv, file_name="rekap_wind_2021_2025.csv", mime="text/csv", use_container_width=True)
    else:
        st.warning("⚠️ Data angin kosong atau gagal diolah.")

def render_acs_home():
    st.title("✈️ Aviation Climatology Dashboard")
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Deskripsi & Tujuan
        Dashboard operasional klimatologi penerbangan ini memvisualisasikan data **ACS (Aerodrome Climatological Summary)** rata-rata periode **2021–2025**. 
        
        Dashboard ini didesain tidak hanya untuk menyajikan angka, melainkan menjawab krusialitas operasional meteorologi: 
        **"How often does a condition occur?"** (Berapa sering suatu kondisi terjadi?).
        
        Fokus analisis:
        * Frekuensi & Probabilitas Kejadian
        * Distribusi Musiman
        * Interpretasi Meteorologis Otomatis
        * Implikasi Operasional Penerbangan
        """)
    with col2:
        st.info("📊 **Statistik ACS Dashboard**\n\n📅 **Periode Data:** 2021 - 2025\n\n📂 **Total File / Parameter:** 6 Parameter\n\n📈 **Data Integrity:** Original (No Smoothing)\n\n⚙️ **Modul Engine:** Automated Parsing & Robust Data Loader")

# ==========================================
# MODULE 2 FUNCTIONS: DIURNAL SYNOPTIC ENGINE
# ==========================================
def parse_hourly_freq(df, col_names):
    valid_data = []
    for idx, row in df.iterrows():
        try:
            val0 = str(row.iloc[0]).strip()
            val1 = str(row.iloc[1]).strip()
            if val0.replace('.','',1).isdigit() and val1.isdigit():
                hr, yr = float(val0), float(val1)
                if 0 <= hr <= 23 and 2000 < yr < 2100: valid_data.append(row.values)
        except Exception: pass
    if not valid_data: return pd.DataFrame()
    parsed_df = pd.DataFrame(valid_data).iloc[:, :len(col_names)]
    parsed_df.columns = col_names
    for c in col_names: parsed_df[c] = pd.to_numeric(parsed_df[c], errors='coerce').fillna(0)
    return parsed_df

def parse_3hourly(df):
    valid_data = []
    for idx, row in df.iterrows():
        try:
            val0 = str(row.iloc[0]).strip()
            val1 = str(row.iloc[1]).strip()
            if val0.isdigit() and val1.isdigit():
                yr, dt = float(val0), float(val1)
                if 2000 < yr < 2100 and 1 <= dt <= 31: valid_data.append(row.values)
        except Exception: pass
    if not valid_data: return pd.DataFrame()
    parsed_df = pd.DataFrame(valid_data).iloc[:, :13]
    parsed_df.columns = ['Tahun', 'Tanggal', '00', '03', '06', '09', '12', '15', '18', '21', 'Mean', 'Max', 'Min']
    for c in parsed_df.columns: parsed_df[c] = pd.to_numeric(parsed_df[c], errors='coerce').fillna(0)
    return parsed_df

def parse_wind(df):
    valid_data = []
    current_year = 2021
    wind_sectors = ['35-36-01', '02-03-04', '05-06-07', '08-09-10', '11-12-13', '14-15-16', '17-18-19', '20-21-22', '23-24-25', '26-27-28', '29-30-31', '32-33-34']
    for idx, row in df.iterrows():
        val0 = str(row.iloc[0]).strip()
        val1 = str(row.iloc[1]).strip().replace(' ', '')
        if val0.isdigit() and len(val0) == 4: current_year = int(val0)
        if val1 == 'CALM' or val1 == 'VARIABLE' or val1 in wind_sectors:
            yr = int(val0) if val0.isdigit() and len(val0)==4 else current_year
            valid_data.append([yr, val1] + list(row.iloc[2:12].values))
    if not valid_data: return pd.DataFrame()
    parsed_df = pd.DataFrame(valid_data).iloc[:, :12]
    parsed_df.columns = ['Tahun', 'Direction', '1-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-45', '>45', 'Total']
    for c in parsed_df.columns[2:]: parsed_df[c] = pd.to_numeric(parsed_df[c], errors='coerce').fillna(0)
    return parsed_df

@st.cache_data(show_spinner=False)
def load_all_data():
    datasets = {'RH': pd.DataFrame(), 'TempMaxMin': pd.DataFrame(), 'HS': pd.DataFrame(), 'Vis': pd.DataFrame(), 'Wind': pd.DataFrame()}
    files = {
        'RH': ('RH_2021-2025.xlsx', parse_3hourly),
        'TempMaxMin': ('TempMaxMin_2021-2025.xlsx', parse_3hourly),
        'HS': ('HS_2021-2025.xlsx', lambda df: parse_hourly_freq(df, ['Jam', 'Tahun', '<150', '<200', '<300', '<500', '<1000', '<1500'])),
        'Vis': ('Vis_2021-2025.xlsx', lambda df: parse_hourly_freq(df, ['Jam', 'Tahun', '<200', '<400', '<600', '<800', '<1500', '<1800', '<3000', '<5000', '<8000'])),
        'Wind': ('Wind_2021-2025.xlsx', parse_wind)
    }
    for key, (filename, parser) in files.items():
        if os.path.exists(filename):
            all_sheets = []
            try:
                xls = pd.ExcelFile(filename, engine='openpyxl')
                for month_idx, sheet in enumerate(MONTHS_ID):
                    if sheet in xls.sheet_names:
                        df_raw = pd.read_excel(xls, sheet_name=sheet, header=None)
                        df_parsed = parser(df_raw)
                        if not df_parsed.empty:
                            df_parsed['Bulan'] = sheet
                            df_parsed['Bulan_Idx'] = month_idx + 1
                            all_sheets.append(df_parsed)
                if all_sheets: datasets[key] = pd.concat(all_sheets, ignore_index=True)
            except Exception as e: st.error(f"Error memproses {filename}: {str(e)}")
    return datasets

def add_watermark(fig):
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=50), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
    return fig

# ==========================================
# MODULE 3 FUNCTIONS: TACTICAL OPS ENGINE
# ==========================================
def get_robust_session():
    session = requests.Session()
    retry_strategy = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_metar_raw(icao):
    headers = {'User-Agent': 'Mozilla/5.0 OperationalWeatherClient'}
    icao = icao.upper().strip()
    session = get_robust_session()
    try:
        url = "https://web-aviation.bmkg.go.id/web/metar_speci.php"
        res = session.get(url, headers=headers, timeout=7, verify=False)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            clean_html_text = " ".join(soup.get_text().split())
            match = re.search(fr"\b({icao}\s+\d{{6}}Z\s+.*?)(?=[A-Z]{{4}}\s+\d{{6}}Z|=|$)", clean_html_text)
            if match:
                raw_metar = match.group(1).strip()
                if not raw_metar.endswith('='): raw_metar += '='
                return raw_metar, "BMKG Pusat"
    except: pass
    try:
        url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=raw"
        res = session.get(url, headers=headers, timeout=6)
        if res.status_code == 200 and len(res.text.strip()) > 10 and icao in res.text: return res.text.strip(), "NOAA API"
    except: pass
    try:
        url = f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{icao}.TXT"
        res = session.get(url, headers=headers, timeout=6)
        if res.status_code == 200:
            lines = res.text.strip().split('\n')
            if len(lines) > 1 and icao in lines[1]: return lines[1].strip(), "NOAA Server"
    except: pass
    return None, None

def fetch_taf_raw(icao):
    headers = {'User-Agent': 'Mozilla/5.0 OperationalWeatherClient'}
    icao = icao.upper().strip()
    session = get_robust_session()
    try:
        url = "https://web-aviation.bmkg.go.id/web/taf.php"
        res = session.get(url, headers=headers, timeout=7, verify=False)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            clean_html_text = " ".join(soup.get_text().split())
            match = re.search(fr"\b(TAF\s+(?:AMD\s+|COR\s+)?{icao}\s+\d{{6}}Z\s+.*?)(?=TAF\s+(?:AMD\s+|COR\s+)?[A-Z]{{4}}|=|$)", clean_html_text)
            if match:
                raw_taf = match.group(1).strip()
                if not raw_taf.endswith('='): raw_taf += '='
                return raw_taf
    except: pass
    try:
        url = f"https://aviationweather.gov/api/data/taf?ids={icao}&format=raw"
        res = session.get(url, headers=headers, timeout=6)
        if res.status_code == 200 and len(res.text.strip()) > 10 and icao in res.text: return res.text.strip()
    except: pass
    try:
        url = f"https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{icao}.TXT"
        res = session.get(url, headers=headers, timeout=6)
        if res.status_code == 200:
            lines = res.text.strip().split('\n')
            if len(lines) > 1 and icao in lines[1]: return lines[1].strip()
    except: pass
    return "TAFOR DATA NIL="

def get_data_with_fallback(icao_list):
    for icao in icao_list:
        raw_metar, src = fetch_metar_raw(icao)
        if raw_metar: 
            raw_taf = fetch_taf_raw(icao)
            return raw_metar, raw_taf, src, icao
    return None, None, None, None

def parse_metar(raw, original_icao):
    data = {"wind": "NIL", "vis": "NIL", "wx": "NIL", "cld": "NIL", "tt_td": "NIL", "qnh": "1013/29.92", "qfe": "NIL", "trend": "NOSIG", "rmk": "NIL"}
    if not raw: return data
    main_part = raw
    if "RMK" in raw:
        main_part, rmk_part = raw.split("RMK", 1)
        data["rmk"] = rmk_part.replace("=", "").strip()
    trend_search = re.search(r'\b(TEMPO|BECMG|NOSIG)\b(.*)', main_part)
    if trend_search:
        trend_type = trend_search.group(1)
        trend_rest = trend_search.group(2).replace("=", "").strip()
        data["trend"] = "NOSIG" if trend_type == "NOSIG" else f"{trend_type} {trend_rest}".strip()
        main_part = main_part[:trend_search.start()].strip()
    main_part = main_part.replace("=", "").strip()
    w = re.search(r'\b(\d{3}|VRB)(\d{2,3})(G\d{2,3})?KT\b', main_part)
    if w:
        gust = w.group(3) if w.group(3) else ""
        data["wind"] = f"{w.group(1)}/{w.group(2)}{gust} KT"
    v_match = re.search(r'\b(\d{4})\b', main_part)
    if v_match:
        dist = int(v_match.group(1))
        data["vis"] = "10 KM" if dist == 9999 else f"{dist} M"
    elif "CAVOK" in main_part: data["vis"] = "10 KM"
    wx_codes = r'(?:VC|MI|BC|PR|DR|BL|SH|TS|FZ|DZ|RA|SN|SG|IC|PL|GR|GS|UP|BR|FG|FU|VA|DU|SA|HZ|PY|PO|SQ|FC|SS|DS)'
    all_wx = re.findall(fr'\b([-+]?(?:{wx_codes})+)\b', main_part)
    all_wx = [x for x in all_wx if x not in [original_icao, "TEMPO", "BECMG", "NOSIG"]]
    data["wx"] = " ".join(all_wx) if all_wx else "NIL"
    c_layers = re.findall(r'\b(FEW|SCT|BKN|OVC|NSC|SKC)(\d{3})(CB|TCU)?\b', main_part)
    if c_layers: data["cld"] = " ".join([f"{t} {int(h)*100} FT{'' if not c else ' '+c}" for t, h, c in c_layers])
    elif "CAVOK" in main_part: data["cld"] = "NIL"
    tt_td = re.search(r'\b(M?\d{2})/(M?\d{2})\b', main_part)
    if tt_td: data["tt_td"] = f"{tt_td.group(1).replace('M','-')}/{tt_td.group(2).replace('M','-')}"
    q = re.search(r'\bQ(\d{4})\b', main_part)
    if q:
        val = int(q.group(1))
        data["qnh"] = f"{val}/{val*0.02953:.2f}"
        data["qfe"] = "NIL"  
    return data

class QAM_PDF(FPDF):
    def header(self):
        self.set_font("helvetica", 'B', 11)
        self.cell(0, 5, "MARKAS BESAR ANGKATAN UDARA", ln=True, align='L')
        self.cell(0, 5, "DINAS PENGEMBANGAN OPERASI", ln=True, align='L')
        self.ln(6)
        self.set_font("helvetica", 'BU', 12)
        self.cell(0, 6, "METEOROLOGICAL REPORT FOR TAKE OFF AND LANDING", ln=True, align='C')
        self.ln(6)

def generate_pdf(data, raw_taf, icao, name=""):
    pdf = QAM_PDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 10)
    date_str = datetime.utcnow().strftime('%d-%m-%Y')
    time_str = datetime.utcnow().strftime('%H.%M')
    pdf.cell(0, 6, f"METEOROLOGICAL OBS AT      DATE {date_str}      TIME {time_str} (UTC)", ln=True)
    pdf.ln(3)
    def get_multicell_lines(text, max_width):
        lines = 0
        for paragraph in text.split('\n'):
            words = paragraph.split(' ')
            current_line = ""
            for word in words:
                if pdf.get_string_width(current_line + word + " ") > max_width:
                    lines += 1
                    current_line = word + " "
                else: current_line += word + " "
            lines += 1
        return lines
    def add_fixed_row(label_lines, value_lines, h):
        x = pdf.get_x()
        y = pdf.get_y()
        if y + h > 270:
            pdf.add_page()
            x = pdf.get_x()
            y = pdf.get_y()
        pdf.rect(x, y, 95, h)
        pdf.rect(x + 95, y, 95, h)
        pdf.set_font("helvetica", 'B', 10)
        pdf.set_xy(x + 2, y + 2)
        for line in label_lines: pdf.cell(91, 5, line, ln=2)
        pdf.set_font("helvetica", '', 10)
        pdf.set_xy(x + 97, y + 2)
        for line in value_lines: pdf.cell(91, 5, line, ln=2)
        pdf.set_xy(x, y + h)
    add_fixed_row(["AERODROME IDENTIFICATION"], [icao], 10)
    add_fixed_row(["SURFACE WIND DIRECTION, SPEED", "AND SIGNIFICANT VARIATION"], [data['wind']], 12)
    add_fixed_row(["HORIZONTAL VISIBILITY"], [data['vis']], 10)
    add_fixed_row(["RUNWAY VISUAL RANGE"], ["NIL"], 10)
    add_fixed_row(["PRESENT WEATHER"], [data['wx']], 10)
    add_fixed_row(["AMOUNT AND HEIGHT OF BASE", "OF LOW CLOUD"], [data['cld']], 12)
    add_fixed_row(["AIR TEMPERATURE AND", "DEW POINT TEMPERATURE"], [data['tt_td']], 12)
    add_fixed_row(["QNH"], [data['qnh']], 10)
    add_fixed_row(["QFE*"], [data['qfe']], 10)
    pdf.set_font("helvetica", '', 10)
    supp_label = "SUPPLEMENTARY\nINFORMATION"
    supp_val = f"RMK: {data['rmk']}\nTREND: {data['trend']}\n\nTAFOR:\n{raw_taf}"
    h_supp = max(15, get_multicell_lines(supp_val, 91) * 5 + 4)
    x = pdf.get_x()
    y = pdf.get_y()
    if y + h_supp > 270:
        pdf.add_page()
        x = pdf.get_x()
        y = pdf.get_y()
    pdf.rect(x, y, 95, h_supp)
    pdf.rect(x + 95, y, 95, h_supp)
    pdf.set_font("helvetica", 'B', 10)
    pdf.set_xy(x + 2, y + 2)
    pdf.multi_cell(91, 5, supp_label)
    pdf.set_font("helvetica", '', 10)
    pdf.set_xy(x + 97, y + 2)
    pdf.multi_cell(91, 5, supp_val)
    pdf.set_xy(x, y + h_supp)
    pdf.ln(8)
    pdf.set_font("helvetica", 'B', 10)
    pdf.cell(95, 5, "TIME OF ISSUE ............................ (UTC)", ln=0)
    pdf.cell(95, 5, "OBSERVER ........................................", ln=1, align='R')
    pdf.cell(95, 5, "*ON REQUEST", ln=1)
    return bytes(pdf.output())

def generate_pdf(p_data, raw_taf, icao, display_name):
    # =========================================================================
    # PERTAHANKAN SELURUH SCRIPT ASLI ANDA DI SINI
    # (Inisialisasi FPDF, add_page, set_font, cell, multi_cell, tabel, dll.)
    # =========================================================================
    
    # -------------------------------------------------------------------------
    # [PERBAIKAN] Blok Output PDF Anti-Crash & Tahan Banting (Pengganti Baris 825)
    # -------------------------------------------------------------------------
    try:
        # Mencoba keluaran standar (Kompatibel dengan fpdf2 modern)
        pdf_out = pdf.output()
    except TypeError:
        # Menangani fallback jika menggunakan pustaka fpdf klasik
        pdf_out = pdf.output(dest='S')
        
    # Evaluasi tipe data dan konversi aman ke tipe bytes
    if isinstance(pdf_out, str):
        # Jika output berupa string, lakukan encode latin-1 agar tidak TypeError
        return pdf_out.encode('latin-1', errors='replace')
    elif isinstance(pdf_out, (bytearray, bytes)):
        # Jika sudah berupa bytearray/bytes (fpdf2), langsung kembalikan
        return bytes(pdf_out)
    else:
        # Safety net untuk tipe data lain
        return str(pdf_out).encode('latin-1', errors='replace')
