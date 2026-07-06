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

def fetch_metar():
    r = requests.get(METAR_API, params={"ids": "WIBB", "hours": 0}, timeout=10)
    r.raise_for_status()
    return r.text.strip()

def fetch_metar_history(hours=24):
    r = requests.get(METAR_API, params={"ids": "WIBB", "hours": hours}, timeout=10)
    r.raise_for_status()
    return r.text.strip().splitlines()

def fetch_metar_ogimet(hours=24):
    end = datetime.utcnow()
    start = end - pd.Timedelta(hours=hours)
    url = "https://www.ogimet.com/display_metars2.php"
    params = {"lang": "en", "lugar": "WIBB", "tipo": "ALL", "ord": "REV", "nil": "NO", "fmt": "txt", "ano": start.year, "mes": start.month, "day": start.day, "hora": start.hour, "anof": end.year, "mesf": end.month, "dayf": end.day, "horaf": end.hour, "minf": end.minute}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return [l.strip() for l in r.text.splitlines() if l.startswith("WIBB")]

def wind(m):
    x = re.search(r'(\d{3})(\d{2})KT', m)
    return f"{x.group(1)}° / {x.group(2)} kt" if x else "-"

def visibility(m):
    x = re.search(r' (\d{4}) ', m)
    return f"{x.group(1)} m" if x else "-"

def temp_dew(m):
    x = re.search(r' (M?\d{2})/(M?\d{2})', m)
    return f"{x.group(1)} / {x.group(2)} °C" if x else "-"

def qnh(m):
    x = re.search(r' Q(\d{4})', m)
    return f"{x.group(1)} hPa" if x else "-"

def parse_numeric_metar(m):
    t = re.search(r' (\d{2})(\d{2})(\d{2})Z', m)
    if not t: return None
    data = {"time": datetime.strptime(t.group(0).strip(), "%d%H%MZ"), "wind": None, "temp": None, "dew": None, "qnh": None, "vis": None, "RA": "RA" in m, "TS": "TS" in m, "FG": "FG" in m}
    w = re.search(r'(\d{3})(\d{2})KT', m)
    if w: data["wind"] = int(w.group(2))
    td = re.search(r' (M?\d{2})/(M?\d{2})', m)
    if td:
        data["temp"] = int(td.group(1).replace("M", "-"))
        data["dew"] = int(td.group(2).replace("M", "-"))
    q = re.search(r' Q(\d{4})', m)
    if q: data["qnh"] = int(q.group(1))
    v = re.search(r' (\d{4}) ', m)
    if v: data["vis"] = int(v.group(1))
    return data

def generate_raw_pdf(lines):
    content = "BT\n/F1 10 Tf\n72 800 Td\n"
    for l in lines:
        safe = l.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        content += f"({safe}) Tj\n0 -14 Td\n"
    content += "ET"
    return (
        b"%PDF-1.4\n1 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n"
        b"2 0 obj<< /Length " + str(len(content)).encode() + b" >>stream\n" + content.encode() +
        b"\nendstream endobj\n3 0 obj<< /Type /Page /Parent 4 0 R /Contents 2 0 R "
        b"/Resources<< /Font<< /F1 1 0 R >> >> >>endobj\n4 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 "
        b"/MediaBox [0 0 595 842] >>endobj\n5 0 obj<< /Type /Catalog /Pages 4 0 R >>endobj\nxref\n0 6\n0000000000 65535 f \n"
        b"trailer<< /Size 6 /Root 5 0 R >>\n%%EOF"
    )

@st.cache_data(ttl=300)
def fetch_forecast(adm1: str):
    params = {"adm1": adm1}
    resp = requests.get(API_BASE, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def flatten_cuaca_entry(entry):
    rows = []
    lokasi = entry.get("lokasi", {})
    for group in entry.get("cuaca", []):
        for obs in group:
            r = obs.copy()
            r.update({"adm1": lokasi.get("adm1"), "adm2": lokasi.get("adm2"), "provinsi": lokasi.get("provinsi"), "kotkab": lokasi.get("kotkab"), "lon": lokasi.get("lon"), "lat": lokasi.get("lat")})
            try:
                r["utc_datetime_dt"] = pd.to_datetime(r.get("utc_datetime"))
                r["local_datetime_dt"] = pd.to_datetime(r.get("local_datetime"))
            except Exception:
                r["utc_datetime_dt"], r["local_datetime_dt"] = pd.NaT, pd.NaT
            rows.append(r)
    df = pd.DataFrame(rows)
    for c in ["t", "tcc", "tp", "wd_deg", "ws", "hu", "vs"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

# ==========================================
# 4. MASTER FLOATING SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("### 🧭 COMMAND NAVIGATOR")
app_mode = st.sidebar.radio(
    "Pilih Modul Operasional:",
    [
        "1️⃣ ACS Climatology (2021-2025)",
        "2️⃣ Diurnal Synoptic Analysis",
        "3️⃣ Tactical Weather Ops (Real-Time)"
    ]
)
st.sidebar.markdown("---")

# ==========================================
# ROUTER & HERO SECTION DISPLAY
# ==========================================
now_wib = datetime.now().strftime("%d %b %Y | %H:%M WIB")

if app_mode == "1️⃣ ACS Climatology (2021-2025)":
    st.markdown(f"""
    <div class="hero-container">
        <div>
            <h1 class="hero-title">✈️ AVIATION CLIMATOLOGY DASHBOARD</h1>
            <div class="hero-subtitle">Aerodrome Climatological Summary (ACS) Multi-Year Average Analysis</div>
        </div>
        <div>
            <div class="status-badge">ONLINE • CLIMATOLOGY ARCHIVE</div>
            <div style="font-size:11px; color:#94A3B8; text-align:right; margin-top:6px;">SYNC: {now_wib}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("#### Parameter ACS")
    menu = st.sidebar.radio("", [
        "Home", "Temperature Frequency", "Temperature Mean Max Min", 
        "Relative Humidity", "Visibility", "Cloud Base (HS)", "Wind"
    ])
    
    if menu == "Home": render_acs_home()
    elif menu == "Temperature Frequency": render_generic_page("🌡️ Temperature Frequency", "rekap_temperature_2021_2025.xlsx", "Temperature Freq", 'bar', "Reds", "Kategori Suhu (°C)")
    elif menu == "Temperature Mean Max Min": render_generic_page("📈 Temperature Mean Max Min", "rekap_temp_max_min_2021_2025.xlsx", "Temperature Mean", 'line', "Reds", "Parameter Suhu")
    elif menu == "Relative Humidity": render_generic_page("💧 Relative Humidity", "rekap_rh_max_min_2021_2025.xlsx", "Relative Humidity", 'line', "Teal", "Waktu Pengamatan (UTC)")
    elif menu == "Visibility": render_generic_page("🌫️ Visibility", "rekap_visibility_2021_2025.xlsx", "Visibility", 'bar', "Greens", "Jarak Pandang (Meter)")
    elif menu == "Cloud Base (HS)": render_generic_page("☁️ Cloud Base (Ceiling)", "rekap_hs_2021_2025.xlsx", "Cloud Base", 'bar', "Blues", "Tinggi Awan (Feet)")
    elif menu == "Wind": render_wind_page()

elif app_mode == "2️⃣ Diurnal Synoptic Analysis":
    st.markdown(f"""
    <div class="hero-container">
        <div>
            <h1 class="hero-title">🌤️ TNI AU DIURNAL METEOROLOGICAL DASHBOARD</h1>
            <div class="hero-subtitle">Ekstraksi Otomatis & Analisis Fluktuasi Permukaan Historis WMO</div>
        </div>
        <div>
            <div class="status-badge">ONLINE • SYNOPTIC ENGINE</div>
            <div style="font-size:11px; color:#94A3B8; text-align:right; margin-top:6px;">SYNC: {now_wib}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Membaca dan menstrukturisasi ulang data Excel WMO..."):
        data = load_all_data()
        
    st.sidebar.markdown("#### Filter Synoptic")
    param_options = {
        "Temperature": "Suhu Udara (°C) [Synoptic]",
        "RH": "Kelembapan Relatif (%) [Synoptic]",
        "Visibility": "Jarak Pandang (Km) [Frequencies]",
        "Cloud Base (HS)": "Tinggi Dasar Awan [Frequencies]",
        "Wind": "Mawar Angin (Wind Rose)"
    }
    selected_param = st.sidebar.selectbox("Pilih Parameter Utama", list(param_options.keys()), format_func=lambda x: param_options[x])
    month_choice = st.sidebar.selectbox("Pilih Bulan", ["Semua Bulan"] + MONTHS_ID)
    available_years = [2021, 2022, 2023, 2024, 2025]
    selected_year = st.sidebar.selectbox("Pilih Tahun", ["Semua Tahun"] + available_years)

    def filter_df(df):
        if df.empty: return df
        res = df.copy()
        if month_choice != "Semua Bulan": res = res[res['Bulan'] == month_choice]
        if selected_year != "Semua Tahun": res = res[res['Tahun'] == int(selected_year)]
        return res

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        t_df = filter_df(data['TempMaxMin'])
        val = f"{t_df['Mean'].mean():.1f} °C" if not t_df.empty else "N/A"
        st.metric("Avg Mean Temperature", val)
    with kpi_cols[1]:
        r_df = filter_df(data['RH'])
        val = f"{r_df['Mean'].mean():.1f} %" if not r_df.empty else "N/A"
        st.metric("Avg Relative Humidity", val)
    with kpi_cols[2]:
        w_df = filter_df(data['Wind'])
        if not w_df.empty:
            calm_pct = w_df[w_df['Direction'] == 'CALM']['Total'].mean()
            val = f"{calm_pct:.1f} %"
        else: val = "N/A"
        st.metric("Rerata Kondisi CALM (Angin)", val)
    with kpi_cols[3]:
        v_df = filter_df(data['Vis'])
        val = f"{v_df['<8000'].mean():.1f} %" if (not v_df.empty and '<8000' in v_df.columns) else "N/A"
        st.metric("Frekuensi Visibilitas < 8Km", val)

    st.markdown("<br>", unsafe_allow_html=True)

    if selected_param == "Temperature":
        st.subheader("Pola Suhu Udara Synoptic (3-Jam-an UTC)")
        df_t = filter_df(data['TempMaxMin'])
        if df_t.empty: st.warning("Data Suhu belum/tidak diunggah.")
        else:
            df_melt = df_t.melt(id_vars=['Tahun', 'Bulan_Idx', 'Tanggal'], value_vars=['00', '03', '06', '09', '12', '15', '18', '21'], var_name='Jam_UTC', value_name='Suhu')
            agg_df = df_melt.groupby('Jam_UTC')['Suhu'].mean().reset_index()
            fig = px.line(agg_df, x='Jam_UTC', y='Suhu', markers=True, title=f"Kurva Suhu Diurnal - {month_choice} ({selected_year})", labels={'Jam_UTC': 'Jam Synoptic (UTC)', 'Suhu': 'Temperatur (°C)'})
            fig.update_traces(line=dict(color='#38BDF8', width=3))
            st.plotly_chart(add_watermark(fig), use_container_width=True)

    elif selected_param == "RH":
        st.subheader("Pola Kelembapan Relatif (RH) Synoptic")
        df_r = filter_df(data['RH'])
        if df_r.empty: st.warning("Data RH belum/tidak diunggah.")
        else:
            df_melt = df_r.melt(id_vars=['Tahun', 'Bulan_Idx', 'Tanggal'], value_vars=['00', '03', '06', '09', '12', '15', '18', '21'], var_name='Jam_UTC', value_name='RH')
            agg_df = df_melt.groupby('Jam_UTC')['RH'].mean().reset_index()
            fig = px.line(agg_df, x='Jam_UTC', y='RH', markers=True, title=f"Kurva RH Diurnal - {month_choice} ({selected_year})", labels={'Jam_UTC': 'Jam Synoptic (UTC)', 'RH': 'Kelembapan (%)'})
            fig.update_traces(line=dict(color='#38BDF8', width=3))
            fig.update_layout(yaxis=dict(range=[40, 105]))
            st.plotly_chart(add_watermark(fig), use_container_width=True)

    elif selected_param == "Visibility":
        st.subheader("Meteogram Fluktuasi Diurnal Jarak Pandang (Visibility)")
        df_v = filter_df(data['Vis'])
        if df_v.empty: st.warning("Data Visibilitas tidak ditemukan.")
        else:
            cols = ['<200', '<400', '<600', '<800', '<1500', '<1800', '<3000', '<5000', '<8000']
            agg_v = df_v.groupby('Jam')[cols].mean().reset_index().sort_values('Jam')
            hm_df = agg_v.melt(id_vars='Jam', value_vars=cols, var_name='Kategori_Vis', value_name='Frekuensi')
            vibrant_palette = ["#EF4444", "#38BDF8", "#22C55E", "#FACC15", "#A855F7", "#06B6D4", "#F97316", "#8B5CF6", "#F8FAFC"]
            fig = px.line(hm_df, x='Jam', y='Frekuensi', color='Kategori_Vis', markers=True, title=f"Meteogram Fluktuasi Frekuensi Jarak Pandang - {month_choice} ({selected_year})", labels={'Jam': 'Jam Synoptic (UTC)', 'Frekuensi': 'Frekuensi Kejadian (%)', 'Kategori_Vis': 'Batas Visibilitas (m)'}, color_discrete_sequence=vibrant_palette)
            fig.update_traces(line=dict(width=3), marker=dict(size=7))
            fig.update_layout(hovermode="x unified", xaxis=dict(tickmode='linear', tick0=0, dtick=1, range=[-0.5, 23.5]), yaxis=dict(rangemode='tozero', gridcolor='rgba(255,255,255,0.08)'), legend=dict(title="Kategori Visibilitas", orientation="v", yanchor="top", y=1, xanchor="left", x=1.02))
            st.plotly_chart(add_watermark(fig), use_container_width=True)

    elif selected_param == "Cloud Base (HS)":
        st.subheader("Meteogram Fluktuasi Diurnal Tinggi Dasar Awan (Ceiling)")
        df_hs = filter_df(data['HS'])
        if df_hs.empty: st.warning("Data Cloud Base tidak ditemukan.")
        else:
            cols = ['<150', '<200', '<300', '<500', '<1000', '<1500']
            agg_hs = df_hs.groupby('Jam')[cols].mean().reset_index().sort_values('Jam')
            hm_df = agg_hs.melt(id_vars='Jam', value_vars=cols, var_name='Kategori_HS', value_name='Frekuensi')
            vibrant_palette_hs = ["#F97316", "#38BDF8", "#14B8A6", "#A855F7", "#EC4899", "#64748B"]
            fig = px.line(hm_df, x='Jam', y='Frekuensi', color='Kategori_HS', markers=True, title=f"Meteogram Fluktuasi Frekuensi Tinggi Dasar Awan - {month_choice} ({selected_year})", labels={'Jam': 'Jam Synoptic (UTC)', 'Frekuensi': 'Frekuensi Kejadian (%)', 'Kategori_HS': 'Tinggi Awan (ft)'}, color_discrete_sequence=vibrant_palette_hs)
            fig.update_traces(line=dict(width=3), marker=dict(size=7))
            fig.update_layout(hovermode="x unified", xaxis=dict(tickmode='linear', tick0=0, dtick=1, range=[-0.5, 23.5]), yaxis=dict(rangemode='tozero', gridcolor='rgba(255,255,255,0.08)'), legend=dict(title="Kategori Ceiling (ft)", orientation="v", yanchor="top", y=1, xanchor="left", x=1.02))
            st.plotly_chart(add_watermark(fig), use_container_width=True)

    elif selected_param == "Wind":
        st.subheader("Mawar Angin (Wind Rose) Multi-sektor")
        df_w = filter_df(data['Wind'])
        if df_w.empty: st.warning("Data Wind tidak ditemukan.")
        else:
            dir_map = {'35-36-01': 'Utara (N)', '02-03-04': 'Timur Laut (NNE)', '05-06-07': 'Timur Laut (ENE)', '08-09-10': 'Timur (E)', '11-12-13': 'Tenggara (ESE)', '14-15-16': 'Tenggara (SSE)', '17-18-19': 'Selatan (S)', '20-21-22': 'Barat Daya (SSW)', '23-24-25': 'Barat Daya (WSW)', '26-27-28': 'Barat (W)', '29-30-31': 'Barat Laut (WNW)', '32-33-34': 'Barat Laut (NNW)'}
            compass_order = ['Utara (N)', 'Timur Laut (NNE)', 'Timur Laut (ENE)', 'Timur (E)', 'Tenggara (ESE)', 'Tenggara (SSE)', 'Selatan (S)', 'Barat Daya (SSW)', 'Barat Daya (WSW)', 'Barat (W)', 'Barat Laut (WNW)', 'Barat Laut (NNW)']
            rose_df = df_w[~df_w['Direction'].isin(['CALM', 'VARIABLE'])].copy()
            if not rose_df.empty:
                rose_df['Direction_Label'] = rose_df['Direction'].map(dir_map)
                speed_cols = ['1-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-45', '>45']
                melted_rose = rose_df.melt(id_vars=['Direction_Label'], value_vars=speed_cols, var_name='Speed_Knot', value_name='Frequency')
                agg_rose = melted_rose.groupby(['Direction_Label', 'Speed_Knot'])['Frequency'].mean().reset_index()
                agg_rose = agg_rose[agg_rose['Frequency'] > 0]
                fig = px.bar_polar(agg_rose, r="Frequency", theta="Direction_Label", color="Speed_Knot", color_discrete_sequence=px.colors.sequential.Plasma_r, title="Distribusi Arah dan Kecepatan Angin (Knots)")
                fig.update_layout(polar=dict(angularaxis=dict(direction="clockwise", categoryorder="array", categoryarray=compass_order, rotation=90)), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
                st.plotly_chart(fig, use_container_width=True)
            calm_df = df_w[df_w['Direction'].isin(['CALM', 'VARIABLE'])]
            if not calm_df.empty:
                st.caption("Catatan Kondisi Khusus:")
                st.dataframe(calm_df.groupby('Direction')['Total'].mean().reset_index().rename(columns={'Total': 'Persentase Kejadian (%)'}))

elif app_mode == "3️⃣ Tactical Weather Ops (Real-Time)":
    st.markdown(f"""
    <div class="hero-container">
        <div>
            <h1 class="hero-title">🛰️ TACTICAL WEATHER OPERATIONS — BMKG</h1>
            <div class="hero-subtitle">Real-Time METAR/TAFOR Intelligence & Automated Flight Dispatch QAM</div>
        </div>
        <div>
            <div class="status-badge">ONLINE • LIVE RADAR LINK</div>
            <div style="font-size:11px; color:#94A3B8; text-align:right; margin-top:6px;">SYNC: {now_wib}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("#### Tactical Controls")
    provinsi_list = list(PROVINCE_ADM1_MAP.keys())
    default_idx = provinsi_list.index("Riau (14)") if "Riau (14)" in provinsi_list else 0
    selected_prov_label = st.sidebar.selectbox("📍 Province Code (ADM1)", options=provinsi_list, index=default_idx)
    adm1 = PROVINCE_ADM1_MAP[selected_prov_label]
    
    st.sidebar.markdown("<div class='radar'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align:center; color:#38BDF8; font-weight:600; font-size:12px;'>SCANNING WEATHER RADAR...</p>", unsafe_allow_html=True)
    refresh = st.sidebar.button("🔄 Fetch Data")
    st.sidebar.markdown("---")
    show_map = st.sidebar.checkbox("Show Map", value=True)
    show_table = st.sidebar.checkbox("Show Table", value=False)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📡 QAM Multi-Station", "📝 QAM Manual", "📊 WIBB METAR & History", "🛰️ BMKG Tactical Forecast"
    ])

    with tab1:
        st.info("Penarikan data METAR real-time dengan sistem Fallback Terdekat.")
        col1, col2 = st.columns([1, 1])
        with col1:
            pilihan = st.selectbox("Pilih Pangkalan / Lanud:", list(sorted(LANUD_MAP.keys())))
            icao_list = LANUD_MAP[pilihan]
            display_name = pilihan.split(" (")[0].replace("Lanud ", "")
            generate_btn = st.button("TARIK DATA & GENERATE QAM", use_container_width=True)
        with col2:
            st.info("Status Jaringan: Multi-Source (BMKG/NOAA/Nearby)")
        if generate_btn:
            with st.spinner(f"Menghubungi server untuk {icao_list[0]}..."):
                raw_text, raw_taf, source, found_icao = get_data_with_fallback(icao_list)
                if raw_text:
                    if found_icao != icao_list[0]:
                        st.warning(f"Data {icao_list[0]} Offline. Menggunakan data stasiun terdekat: {found_icao}")
                    st.success(f"BERHASIL (Sumber: {source})")
                    st.code(f"// RAW METAR DATA\n{raw_text}\n\n// RAW TAFOR FORECAST DATA\n{raw_taf}")
                    p_data = parse_metar(raw_text, icao_list[0])
                    pdf_bytes = generate_pdf(p_data, raw_taf, icao_list[0], display_name)
                    st.download_button(label=f"📥 DOWNLOAD PDF QAM - {icao_list[0]}", data=pdf_bytes, file_name=f"QAM_{icao_list[0]}_{datetime.now().strftime('%H%M')}.pdf", mime="application/pdf", use_container_width=True)
                else: st.error("Semua server (Utama & Terdekat) tidak merespon. Coba beberapa saat lagi.")

    with tab2:
        st.info("Input sandi observasi secara manual jika terjadi pemutusan jaringan komunikasi.")
        with st.form("form_manual_qam"):
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                man_icao = st.text_input("AERODROME IDENTIFICATION (ICAO)", "WIBB")
                man_wind = st.text_input("SURFACE WIND (Dir/Speed)", "VRB02KT")
                man_vis = st.text_input("HORIZONTAL VISIBILITY", "8000 M")
                man_wx = st.text_input("PRESENT WEATHER", "NIL")
                man_cld = st.text_input("CLOUD (Amount & Height)", "FEW 015")
            with col_m2:
                man_tt_td = st.text_input("AIR TEMP / DEW POINT", "33/24")
                man_qnh = st.text_input("QNH (hPa/inHg)", "1010/29.83")
                man_qfe = st.text_input("QFE", "NIL")
                man_trend = st.text_input("TREND", "NOSIG")
                man_rmk = st.text_input("REMARKS (RMK)", "NIL")
            man_taf = st.text_area("TAFOR FORECAST DATA", "TAF WIBB 130500Z 1306/1406 ...")
            btn_manual_generate = st.form_submit_button("GENERATE PDF MANUAL", use_container_width=True)
        if btn_manual_generate:
            manual_data_dict = {"wind": man_wind, "vis": man_vis, "wx": man_wx, "cld": man_cld, "tt_td": man_tt_td, "qnh": man_qnh, "qfe": man_qfe, "trend": man_trend, "rmk": man_rmk}
            pdf_bytes_manual = generate_pdf(manual_data_dict, man_taf, man_icao)
            st.success("Dokumen QAM Manual Berhasil Di-generate!")
            st.download_button(label=f"📥 DOWNLOAD PDF QAM MANUAL - {man_icao}", data=pdf_bytes_manual, file_name=f"QAM_MANUAL_{man_icao}_{datetime.now().strftime('%H%M')}.pdf", mime="application/pdf", use_container_width=True)

    with tab3:
        st.subheader("Lanud Roesmin Nurjadin — WIBB")
        now = datetime.now(timezone.utc).strftime("%d %b %Y %H%M UTC")
        try:
            metar_txt = fetch_metar()
            qam_text = ["METEOROLOGICAL REPORT (QAM)", f"DATE / TIME (UTC) : {now}", "AERODROME        : WIBB", f"SURFACE WIND     : {wind(metar_txt)}", f"VISIBILITY       : {visibility(metar_txt)}", f"TEMP / DEWPOINT  : {temp_dew(metar_txt)}", f"QNH              : {qnh(metar_txt)}", "", "RAW METAR:", metar_txt]
            st.download_button("⬇️ Download QAM Text (PDF)", data=generate_raw_pdf(qam_text), file_name="QAM_WIBB_TEXT.pdf", mime="application/pdf")
            st.code(metar_txt)
        except Exception as e: st.error("Gagal menarik data WIBB METAR terkini.")
        st.divider()
        st.subheader("🛰️ Weather Satellite — Himawari-8 (Infrared)")
        st.caption("BMKG Himawari-8 | Reference only — not for tactical separation")
        try:
            img = requests.get(SATELLITE_HIMA_RIAU, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            img.raise_for_status()
            st.image(img.content, use_container_width=True)
        except Exception: st.warning("Satellite imagery temporarily unavailable.")
        st.divider()
        st.subheader("📊 Historical METAR Meteogram — Last 24h")
        try:
            raw_hist = fetch_metar_history(24)
            source_hist = "AviationWeather.gov"
            if not raw_hist or len(raw_hist) < 2:
                raw_hist = fetch_metar_ogimet(24)
                source_hist = "OGIMET Archive"
            df_hist = pd.DataFrame([parse_numeric_metar(m) for m in raw_hist if parse_numeric_metar(m)])
            st.caption(f"Data source: {source_hist} | Records: {len(df_hist)}")
            if not df_hist.empty:
                df_hist.sort_values("time", inplace=True)
                fig = make_subplots(rows=5, cols=1, shared_xaxes=True, subplot_titles=["Temperature / Dew Point (°C)","Wind Speed (kt)","QNH (hPa)","Visibility (m)","Weather Flags (RA / TS / FG)"])
                fig.add_trace(go.Scatter(x=df_hist["time"], y=df_hist["temp"], name="Temp"), 1, 1)
                fig.add_trace(go.Scatter(x=df_hist["time"], y=df_hist["dew"], name="Dew"), 1, 1)
                fig.add_trace(go.Scatter(x=df_hist["time"], y=df_hist["wind"], name="Wind"), 2, 1)
                fig.add_trace(go.Scatter(x=df_hist["time"], y=df_hist["qnh"], name="QNH"), 3, 1)
                fig.add_trace(go.Scatter(x=df_hist["time"], y=df_hist["vis"], name="Visibility"), 4, 1)
                fig.add_trace(go.Scatter(x=df_hist["time"], y=df_hist["RA"].astype(int), mode="markers", name="RA"), 5, 1)
                fig.add_trace(go.Scatter(x=df_hist["time"], y=df_hist["TS"].astype(int), mode="markers", name="TS"), 5, 1)
                fig.add_trace(go.Scatter(x=df_hist["time"], y=df_hist["FG"].astype(int), mode="markers", name="FG"), 5, 1)
                fig.update_layout(height=950, hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
                st.plotly_chart(fig, use_container_width=True)
                df_hist["time"] = df_hist["time"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                st.download_button("⬇️ Download CSV", df_hist.to_csv(index=False), "WIBB_METAR_24H.csv")
        except Exception as e: st.warning("Data riwayat METAR tidak tersedia.")

    with tab4:
        st.markdown("*Source: BMKG Forecast API — Live Data*")
        with st.spinner("🛰️ Acquiring weather intelligence..."):
            try:
                raw_fcst = fetch_forecast(adm1)
                entries = raw_fcst.get("data", [])
                if not entries: st.warning("No forecast data available.")
                else:
                    mapping = {}
                    for e in entries:
                        lok = e.get("lokasi", {})
                        label = lok.get("kotkab") or lok.get("adm2") or f"Location {len(mapping)+1}"
                        mapping[label] = {"entry": e}
                    col1, col2 = st.columns([2, 1])
                    with col1: loc_choice = st.selectbox("🎯 Select Location", options=list(mapping.keys()))
                    with col2: st.metric("📍 Locations", len(mapping))
                    selected_entry = mapping[loc_choice]["entry"]
                    df_fcst = flatten_cuaca_entry(selected_entry)
                    if not df_fcst.empty:
                        df_fcst["ws_kt"] = df_fcst["ws"] * MS_TO_KT
                        df_fcst = df_fcst.sort_values("utc_datetime_dt")
                        min_dt = df_fcst["local_datetime_dt"].dropna().min().to_pydatetime()
                        max_dt = df_fcst["local_datetime_dt"].dropna().max().to_pydatetime()
                        start_dt = st.slider("Time Range (Local)", min_value=min_dt, max_value=max_dt, value=(min_dt, max_dt), step=pd.Timedelta(hours=3))
                        mask = (df_fcst["local_datetime_dt"] >= pd.to_datetime(start_dt[0])) & (df_fcst["local_datetime_dt"] <= pd.to_datetime(start_dt[1]))
                        df_sel = df_fcst.loc[mask].copy()
                        st.markdown("---")
                        st.subheader("⚡ Tactical Weather Status")
                        now_fcst = df_sel.iloc[0]
                        c1, c2, c3, c4 = st.columns(4)
                        with c1: st.metric("TEMP (°C)", f"{now_fcst.get('t', '—')}°C")
                        with c2: st.metric("HUMIDITY", f"{now_fcst.get('hu', '—')}%")
                        with c3: st.metric("WIND (KT)", f"{now_fcst.get('ws_kt', 0):.1f}")
                        with c4: st.metric("RAIN (mm)", f"{now_fcst.get('tp', '—')}")
                        st.markdown("---")
                        st.subheader("📊 Parameter Trends")
                        c1, c2 = st.columns(2)
                        with c1:
                            fig_t = px.line(df_sel, x="local_datetime_dt", y="t", title="Temperature (°C)", markers=True, color_discrete_sequence=["#38BDF8"])
                            fig_t.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
                            st.plotly_chart(fig_t, use_container_width=True)
                            fig_h = px.line(df_sel, x="local_datetime_dt", y="hu", title="Humidity (%)", markers=True, color_discrete_sequence=["#22C55E"])
                            fig_h.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
                            st.plotly_chart(fig_h, use_container_width=True)
                        with c2:
                            fig_ws = px.line(df_sel, x="local_datetime_dt", y="ws_kt", title="Wind Speed (KT)", markers=True, color_discrete_sequence=["#22C55E"])
                            fig_ws.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
                            st.plotly_chart(fig_ws, use_container_width=True)
                            fig_tp = px.bar(df_sel, x="local_datetime_dt", y="tp", title="Rainfall (mm)", color_discrete_sequence=["#FACC15"])
                            fig_tp.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
                            st.plotly_chart(fig_tp, use_container_width=True)
                        st.markdown("---")
                        st.subheader("🌪️ Windrose — Direction & Speed")
                        if "wd_deg" in df_sel.columns and "ws_kt" in df_sel.columns:
                            df_wr = df_sel.dropna(subset=["wd_deg", "ws_kt"])
                            if not df_wr.empty:
                                bins_dir = np.arange(-11.25, 360, 22.5)
                                labels_dir = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
                                df_wr["dir_sector"] = pd.cut(df_wr["wd_deg"] % 360, bins=bins_dir, labels=labels_dir, include_lowest=True)
                                speed_bins = [0,5,10,20,30,50,100]
                                speed_labels = ["<5","5–10","10–20","20–30","30–50",">50"]
                                df_wr["speed_class"] = pd.cut(df_wr["ws_kt"], bins=speed_bins, labels=speed_labels, include_lowest=True)
                                freq = df_wr.groupby(["dir_sector","speed_class"], observed=False).size().reset_index(name="count")
                                freq["percent"] = freq["count"]/freq["count"].sum()*100
                                az_map = {"N":0,"NNE":22.5,"NE":45,"ENE":67.5,"E":90,"ESE":112.5,"SE":135,"SSE":157.5,"S":180,"SSW":202.5,"SW":225,"WSW":247.5,"W":270,"WNW":292.5,"NW":315,"NNW":337.5}
                                freq["theta"] = freq["dir_sector"].map(az_map)
                                colors = ["#22C55E","#84CC16","#EAB308","#F97316","#EF4444","#B91C1C"]
                                fig_wr = go.Figure()
                                for i, sc in enumerate(speed_labels):
                                    subset = freq[freq["speed_class"]==sc]
                                    fig_wr.add_trace(go.Barpolar(r=subset["percent"], theta=subset["theta"], name=f"{sc} KT", marker_color=colors[i], opacity=0.85))
                                fig_wr.update_layout(title="Windrose (KT)", polar=dict(angularaxis=dict(direction="clockwise", rotation=90, tickvals=list(range(0,360,45))), radialaxis=dict(ticksuffix="%", showline=True, gridcolor="rgba(255,255,255,0.08)")), legend_title="Wind Speed Class", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
                                st.plotly_chart(fig_wr, use_container_width=True)
                        if show_map:
                            st.markdown("---")
                            st.subheader("🗺️ Tactical Map")
                            try: st.map(pd.DataFrame({"lat": [float(selected_entry.get("lokasi", {}).get("lat", 0))], "lon": [float(selected_entry.get("lokasi", {}).get("lon", 0))]}))
                            except Exception as e: st.warning(f"Map unavailable: {e}")
                        if show_table:
                            st.markdown("---")
                            st.subheader("📋 Forecast Table")
                            st.dataframe(df_sel)
            except Exception as e: st.error(f"Failed to fetch tactical data: {e}")

# Footer
st.markdown("""
---
<div style="text-align:center; color:#64748B; font-size:12px; font-weight:500;">
TNI AU Integrated Tactical Weather System © 2026<br>
Engineered for Operational Aviation Meteorology & Academic Research Excellence
</div>
""", unsafe_allow_html=True)
