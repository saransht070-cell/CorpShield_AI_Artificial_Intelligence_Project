"""
CorpShield AI 🛡️ - Corporate Financial Statement Fraud & Anomaly Surveillance System
Upgraded Full-Stack Architecture conforming to SEBI Investor-Protection Research Objectives.
"""

import os
import json
import io
from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import (
    generate_reproducible_synthetic_dataset,
    generate_csv_template,
    load_public_demo_data
)
from src.data_validation import validate_uploaded_data
from src.anomaly_detection import CorpShieldAnalyzer
from src.model_training import train_and_evaluate_models
from src.report_generator import generate_company_html_dossier
from src.feature_engineering import FEATURE_DEFINITIONS, MODEL_NUMERIC_FEATURES

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & HIGH-TECH SURVEILLANCE STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CorpShield AI 🛡️ | Financial Surveillance Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark navy & cybernetic financial intelligence theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Backgrounds */
    .stApp {
        background-color: #070B19;
        color: #F1F5F9;
    }
    
    /* Top Banner */
    .top-surveillance-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(90deg, rgba(11, 23, 48, 0.95), rgba(7, 11, 25, 0.95));
        border: 1px solid rgba(0, 240, 255, 0.25);
        border-radius: 10px;
        padding: 14px 22px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(0, 240, 255, 0.05);
    }
    .brand-title {
        font-size: 1.7rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00F0FF 0%, #00E5A3 50%, #FFFFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 0.82rem;
        color: #94A3B8;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 229, 163, 0.1);
        border: 1px solid rgba(0, 229, 163, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #00E5A3;
        font-weight: 600;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #00E5A3;
        border-radius: 50%;
        box-shadow: 0 0 8px #00E5A3;
    }

    /* Metric Cards */
    .cyber-metric-card {
        background: #0B132B;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 2px solid #00F0FF;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .cyber-metric-card:hover {
        transform: translateY(-2px);
        border-top-color: #00E5A3;
        box-shadow: 0 8px 25px rgba(0, 240, 255, 0.1);
    }
    .cyber-metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94A3B8;
        font-weight: 600;
    }
    .cyber-metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        margin-top: 4px;
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
    }
    .cyber-metric-sub {
        font-size: 0.72rem;
        color: #64748B;
        margin-top: 4px;
    }

    /* Review Priority Badges */
    .badge-high {
        background: rgba(255, 51, 102, 0.15);
        color: #FF3366;
        border: 1px solid #FF3366;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-moderate {
        background: rgba(255, 184, 0, 0.15);
        color: #FFB800;
        border: 1px solid #FFB800;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-low {
        background: rgba(0, 229, 163, 0.15);
        color: #00E5A3;
        border: 1px solid #00E5A3;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Rule Alert Card */
    .rule-card {
        background: #0B132B;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .rule-card-high { border-left: 4px solid #FF3366; }
    .rule-card-med { border-left: 4px solid #FFB800; }
    .rule-card-low { border-left: 4px solid #00F0FF; }

    /* Forensic Disclaimer */
    .sebi-disclaimer-card {
        background: rgba(11, 19, 43, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 40px;
        font-size: 0.78rem;
        color: #94A3B8;
        line-height: 1.5;
        text-align: center;
    }

    /* Streamlit overrides */
    div[data-testid="stSidebar"] {
        background-color: #050813;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] h2, div[data-testid="stSidebar"] h3 {
        color: #00F0FF;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CACHED INITIALIZATION & RESOURCE MANAGEMENT
# -----------------------------------------------------------------------------
@st.cache_resource
def get_analyzer():
    return CorpShieldAnalyzer(models_dir='models')

def get_plot_layout():
    """Dark cyber layout for Plotly charts"""
    return dict(
        plot_bgcolor="rgba(7, 11, 25, 0.8)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", family="Inter, sans-serif"),
        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.06)", zerolinecolor="rgba(255, 255, 255, 0.1)"),
        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.06)", zerolinecolor="rgba(255, 255, 255, 0.1)"),
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(bgcolor="rgba(11, 19, 43, 0.7)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1)
    )

# Initialize Session State
if 'data_source_mode' not in st.session_state:
    st.session_state['data_source_mode'] = "Synthetic Research Cohort (120 Companies)"
if 'current_df' not in st.session_state:
    # Load default synthetic data
    if os.path.exists('data/synthetic_financials.csv'):
        st.session_state['current_df'] = pd.read_csv('data/synthetic_financials.csv')
    else:
        st.session_state['current_df'] = generate_reproducible_synthetic_dataset(120, 6)
if 'selected_company_for_inspect' not in st.session_state:
    st.session_state['selected_company_for_inspect'] = None

# Ensure models exist
analyzer = get_analyzer()
if not (analyzer.has_if and analyzer.has_rf):
    st.warning("Model weights not detected. Initializing automated training sequence...")
    train_and_evaluate_models()
    st.cache_resource.clear()
    analyzer = get_analyzer()

# Perform initial analysis on current dataframe if not analyzed
if 'composite_risk_score' not in st.session_state['current_df'].columns:
    with st.spinner("Executing CorpShield surveillance pipelines on active cohort..."):
        st.session_state['current_df'] = analyzer.analyze(st.session_state['current_df'])

analyzed_df = st.session_state['current_df']

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & DATA COHORT CONTROLLER
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 10px 0 15px 0;">
    <div style="font-weight: 800; font-size: 1.3rem; color: #00F0FF; letter-spacing: 0.5px;">CORPSHIELD AI</div>
    <div style="font-size: 0.72rem; color: #64748B; font-family: monospace;">FINANCIAL ANOMALY ENGINE</div>
</div>
""", unsafe_allow_html=True)

nav_section = st.sidebar.radio(
    "Surveillance Navigation",
    [
        "1. Command Center",
        "2. Company Risk Analysis",
        "3. Upload & Analyze",
        "4. AI Model Laboratory",
        "5. Financial Reports",
        "6. Data Sources & Methodology"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; font-weight: 700; margin-bottom: 8px;'>Cohort Selector</div>", unsafe_allow_html=True)

cohort_options = [
    "Synthetic Research Cohort (120 Companies)",
    "Public Listed Disclosures (AAPL, MSFT, etc.)",
    "Uploaded Custom Dataset"
]

selected_cohort = st.sidebar.selectbox(
    "Active Financial Dataset",
    cohort_options,
    index=cohort_options.index(st.session_state['data_source_mode']) if st.session_state['data_source_mode'] in cohort_options else 0
)

# Handle cohort switching
if selected_cohort != st.session_state['data_source_mode']:
    st.session_state['data_source_mode'] = selected_cohort
    if selected_cohort == "Synthetic Research Cohort (120 Companies)":
        if os.path.exists('data/synthetic_financials.csv'):
            new_df = pd.read_csv('data/synthetic_financials.csv')
        else:
            new_df = generate_reproducible_synthetic_dataset(120, 6)
        st.session_state['current_df'] = analyzer.analyze(new_df)
    elif selected_cohort == "Public Listed Disclosures (AAPL, MSFT, etc.)":
        pub_df = load_public_demo_data()
        st.session_state['current_df'] = analyzer.analyze(pub_df)
    st.rerun()

st.sidebar.markdown("---")
# Quick rule configuration in sidebar
st.sidebar.markdown("<div style='font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; font-weight: 700; margin-bottom: 8px;'>Surveillance Thresholds</div>", unsafe_allow_html=True)
cfg_rev_thresh = st.sidebar.slider("Rev/OCF Growth Trigger", 0.05, 0.30, 0.10, 0.01, format="%.2f")
cfg_rec_gap = st.sidebar.slider("Receivables Growth Gap Trigger", 0.05, 0.35, 0.15, 0.01, format="%.2f")
cfg_debt_ratio = st.sidebar.slider("Debt-to-Assets Alert Limit", 0.50, 0.90, 0.70, 0.05, format="%.2f")

# -----------------------------------------------------------------------------
# 4. TOP SURVEILLANCE BANNER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="top-surveillance-banner">
    <div>
        <h1 class="brand-title">CORPSHIELD AI 🛡️</h1>
        <div class="brand-subtitle">AI-POWERED CORPORATE FINANCIAL ANOMALY SURVEILLANCE // COHORT: {st.session_state['data_source_mode']}</div>
    </div>
    <div style="display: flex; gap: 12px; align-items: center;">
        <div class="status-pill">
            <div class="status-dot"></div>
            SYSTEM ACTIVE // LOCALHOST:8501
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

df = st.session_state['current_df']

# =============================================================================
# SECTION 1: COMMAND CENTER
# =============================================================================
if nav_section == "1. Command Center":
    st.markdown("### Surveillance Command Center")
    st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 20px; font-size: 0.9rem;'>Real-time analytical metrics derived dynamically from current corporate financial records.</div>", unsafe_allow_html=True)

    # Calculate live KPI metrics
    total_companies = int(df['company_id'].nunique()) if 'company_id' in df.columns else len(df)
    total_periods = len(df)
    high_priority_count = int((df['review_priority'] == 'HIGH').sum())
    mod_priority_count = int((df['review_priority'] == 'MODERATE').sum())
    unsupervised_anomalies = int((df['unsupervised_anomaly_flag'] == 1).sum())
    supervised_flags = int((df['supervised_prediction'] == 1).sum())
    avg_completeness = round(float(df['data_completeness'].mean()), 1) if 'data_completeness' in df.columns else 100.0

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1:
        st.markdown(f"""
        <div class="cyber-metric-card">
            <div class="cyber-metric-label">Monitored Entities</div>
            <div class="cyber-metric-value" style="color: #00F0FF;">{total_companies}</div>
            <div class="cyber-metric-sub">{total_periods} Period Records</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
        <div class="cyber-metric-card" style="border-top-color: #FF3366;">
            <div class="cyber-metric-label">High Priority</div>
            <div class="cyber-metric-value" style="color: #FF3366;">{high_priority_count}</div>
            <div class="cyber-metric-sub">Immediate Review Queue</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
        <div class="cyber-metric-card" style="border-top-color: #FFB800;">
            <div class="cyber-metric-label">Moderate Priority</div>
            <div class="cyber-metric-value" style="color: #FFB800;">{mod_priority_count}</div>
            <div class="cyber-metric-sub">Elevated Watchlist</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
        <div class="cyber-metric-card" style="border-top-color: #00E5A3;">
            <div class="cyber-metric-label">ML Outliers (IF)</div>
            <div class="cyber-metric-value" style="color: #00E5A3;">{unsupervised_anomalies}</div>
            <div class="cyber-metric-sub">Isolation Forest Flags</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi5:
        st.markdown(f"""
        <div class="cyber-metric-card" style="border-top-color: #A855F7;">
            <div class="cyber-metric-label">RF Class Flags</div>
            <div class="cyber-metric-value" style="color: #A855F7;">{supervised_flags}</div>
            <div class="cyber-metric-sub">Simulated Pattern Match</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi6:
        st.markdown(f"""
        <div class="cyber-metric-card" style="border-top-color: #38BDF8;">
            <div class="cyber-metric-label">Completeness</div>
            <div class="cyber-metric-value" style="color: #38BDF8;">{avg_completeness}%</div>
            <div class="cyber-metric-sub">Average Disclosure Index</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Analytical Charts Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Revenue vs. Operating Cash Flow Divergence")
        # Scatter of revenue vs OCF with color by review priority
        color_map = {'HIGH': '#FF3366', 'MODERATE': '#FFB800', 'LOW': '#00E5A3'}
        fig_scatter = px.scatter(
            df,
            x='revenue',
            y='operating_cash_flow',
            color='review_priority',
            color_discrete_map=color_map,
            hover_data=['company_name', 'period', 'composite_risk_score'],
            title="Operating Cash Flow vs. Top-Line Revenue"
        )
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="#FF3366", opacity=0.7)
        fig_scatter.update_layout(get_plot_layout())
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c2:
        st.markdown("##### Receivables vs. Revenue Dynamics")
        # Scatter of revenue vs receivables
        fig_rec = px.scatter(
            df,
            x='revenue',
            y='receivables',
            color='review_priority',
            color_discrete_map=color_map,
            hover_data=['company_name', 'period', 'composite_risk_score'],
            title="Trade Receivables Balance vs. Top-Line Revenue"
        )
        fig_rec.update_layout(get_plot_layout())
        st.plotly_chart(fig_rec, use_container_width=True)

    # Analytical Charts Row 2
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("##### Distribution of Composite Screening Scores")
        fig_hist = px.histogram(
            df,
            x='composite_risk_score',
            nbins=25,
            color='review_priority',
            color_discrete_map=color_map,
            title="Composite Risk Score Spread (0 = Low Risk, 100 = Severe Concern)"
        )
        fig_hist.update_layout(get_plot_layout())
        st.plotly_chart(fig_hist, use_container_width=True)

    with c4:
        st.markdown("##### Cohort Review Priority Breakdown")
        priority_counts = df['review_priority'].value_counts().reset_index()
        priority_counts.columns = ['Priority', 'Count']
        fig_donut = px.pie(
            priority_counts,
            names='Priority',
            values='Count',
            color='Priority',
            color_discrete_map=color_map,
            hole=0.55,
            title="Proportion of Entities by Surveillance Tier"
        )
        fig_donut.update_layout(get_plot_layout())
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Ranked Surveillance Queue
    st.markdown("### Ranked Surveillance Review Queue")
    st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 15px; font-size: 0.85rem;'>Ranked dynamically by Composite Screening Score. Use filters below to target specific sectors or risk tiers.</div>", unsafe_allow_html=True)

    # Filters
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        priority_filter = st.multiselect("Filter by Priority", ['HIGH', 'MODERATE', 'LOW'], default=['HIGH', 'MODERATE'])
    with f_col2:
        period_list = sorted(list(df['period'].astype(str).unique()))
        period_filter = st.multiselect("Filter by Period", period_list, default=period_list)
    with f_col3:
        search_term = st.text_input("Search Company Name / ID", "")

    filtered_df = df.copy()
    if priority_filter:
        filtered_df = filtered_df[filtered_df['review_priority'].isin(priority_filter)]
    if period_filter:
        filtered_df = filtered_df[filtered_df['period'].astype(str).isin(period_filter)]
    if search_term:
        filtered_df = filtered_df[
            filtered_df['company_name'].astype(str).str.contains(search_term, case=False) |
            filtered_df['company_id'].astype(str).str.contains(search_term, case=False)
        ]

    filtered_df = filtered_df.sort_values('composite_risk_score', ascending=False)

    display_cols = [
        'company_id', 'company_name', 'period', 'revenue', 'net_income', 'operating_cash_flow',
        'composite_risk_score', 'review_priority', 'unsupervised_anomaly_score', 'warning_count', 'heuristic_summary'
    ]
    avail_disp = [c for c in display_cols if c in filtered_df.columns]

    st.dataframe(
        filtered_df[avail_disp].style.format({
            'revenue': '₹{:,.0f}' if 'Synthetic' in st.session_state['data_source_mode'] else '{:,.0f}',
            'net_income': '{:,.0f}',
            'operating_cash_flow': '{:,.0f}',
            'composite_risk_score': '{:.1f}',
            'unsupervised_anomaly_score': '{:.1f}'
        }),
        use_container_width=True,
        height=320
    )

    # Quick Jump to Company Risk Analysis
    st.markdown("<br>", unsafe_allow_html=True)
    top_candidates = filtered_df['company_name'].unique().tolist()
    if top_candidates:
        select_jump = st.selectbox("Select entity from queue for comprehensive forensic analysis:", top_candidates)
        if st.button("Deep Dive into Selected Entity ➔"):
            st.session_state['selected_company_for_inspect'] = select_jump
            st.info(f"Navigate to tab '2. Company Risk Analysis' in the left sidebar to inspect {select_jump}.")

# =============================================================================
# SECTION 2: COMPANY RISK ANALYSIS
# =============================================================================
elif nav_section == "2. Company Risk Analysis":
    st.markdown("### Forensic Company Risk Analysis")
    st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 20px; font-size: 0.9rem;'>Detailed forensic audit trail, multi-period financial trajectory, and triggered risk indicators.</div>", unsafe_allow_html=True)

    company_names = sorted(df['company_name'].unique().tolist())
    
    # Pre-select if forwarded from Command Center
    default_idx = 0
    if st.session_state['selected_company_for_inspect'] in company_names:
        default_idx = company_names.index(st.session_state['selected_company_for_inspect'])

    selected_company = st.selectbox("Select Company to Inspect", company_names, index=default_idx)
    company_records = df[df['company_name'] == selected_company].sort_values('period')

    if company_records.empty:
        st.warning("No records found for selected entity.")
    else:
        latest = company_records.iloc[-1]
        c_score = latest.get('composite_risk_score', 0.0)
        c_prio = latest.get('review_priority', 'LOW')
        c_sector = latest.get('sector', 'Corporate General')
        c_source = latest.get('data_source', 'Research Cohort')
        c_auditor = latest.get('auditor_remarks', 'No adverse auditor qualification recorded.')

        # Company Header Card
        p_class = "badge-high" if c_prio == 'HIGH' else ("badge-moderate" if c_prio == 'MODERATE' else "badge-low")
        st.markdown(f"""
        <div style="background: #0B132B; border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 8px; padding: 20px; margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin: 0; color: #FFFFFF; font-size: 1.5rem;">{selected_company}</h2>
                    <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">
                        Sector: <strong>{c_sector}</strong> | Evaluated Periods: <strong>{len(company_records)}</strong> | Source: <strong>{c_source}</strong>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="{p_class}">REVIEW PRIORITY: {c_prio}</span>
                    <div style="font-size: 1.6rem; font-weight: 800; font-family: monospace; color: #00F0FF; margin-top: 6px;">
                        {c_score:.1f} <span style="font-size: 0.85rem; color: #94A3B8;">/ 100</span>
                    </div>
                </div>
            </div>
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255, 255, 255, 0.08); font-size: 0.82rem; color: #CBD5E1;">
                <strong>Statutory Auditor Note / Remarks:</strong> <em>"{c_auditor}"</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Multi-Period Interactive Financial Trajectory
        st.markdown("##### Multi-Period Financial Trajectory")
        fig_trend = go.Figure()
        periods_x = company_records['period'].astype(str).tolist()
        fig_trend.add_trace(go.Scatter(x=periods_x, y=company_records['revenue'], name="Revenue", line=dict(color='#00F0FF', width=3)))
        fig_trend.add_trace(go.Scatter(x=periods_x, y=company_records['net_income'], name="Net Income", line=dict(color='#00E5A3', width=2.5)))
        fig_trend.add_trace(go.Scatter(x=periods_x, y=company_records['operating_cash_flow'], name="Operating Cash Flow", line=dict(color='#FFB800', width=2.5, dash='dash')))
        fig_trend.add_trace(go.Scatter(x=periods_x, y=company_records['receivables'], name="Receivables", line=dict(color='#FF3366', width=2)))
        fig_trend.add_trace(go.Scatter(x=periods_x, y=company_records['debt'], name="Total Debt", line=dict(color='#A855F7', width=2)))
        fig_trend.update_layout(get_plot_layout())
        st.plotly_chart(fig_trend, use_container_width=True)

        # Multi-Period Timeline of Risk Evolution
        st.markdown("##### Risk Progression Timeline Across Reporting Periods")
        timeline_cols = st.columns(len(company_records))
        for idx, (_, p_row) in enumerate(company_records.iterrows()):
            with timeline_cols[idx]:
                p_period = p_row.get('period', f'P{idx+1}')
                p_score = p_row.get('composite_risk_score', 0.0)
                p_prio = p_row.get('review_priority', 'LOW')
                p_warn_cnt = p_row.get('warning_count', 0)
                p_border = "#FF3366" if p_prio == 'HIGH' else ("#FFB800" if p_prio == 'MODERATE' else "#00E5A3")
                st.markdown(f"""
                <div style="background: #0B132B; border: 1px solid rgba(255, 255, 255, 0.08); border-top: 3px solid {p_border}; border-radius: 6px; padding: 12px; text-align: center;">
                    <div style="font-weight: 700; color: #00F0FF; font-size: 0.85rem;">{p_period}</div>
                    <div style="font-size: 1.25rem; font-weight: 800; font-family: monospace; color: #FFFFFF; margin: 4px 0;">{p_score:.1f}</div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">{p_warn_cnt} warnings</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Period Inspector Selector
        period_choice = st.selectbox("Inspect Specific Reporting Period Details", periods_x, index=len(periods_x)-1)
        selected_period_row = company_records[company_records['period'].astype(str) == str(period_choice)].iloc[0]

        row_c1, row_c2 = st.columns([1, 1])
        with row_c1:
            st.markdown("##### Triggered Forensic Warning Rules")
            period_warnings = selected_period_row.get('warnings', [])
            if not period_warnings:
                st.success("No heuristic warning rules triggered for this period.")
            else:
                for w in period_warnings:
                    sev = w.get('severity', 'WARNING')
                    card_cls = "rule-card-high" if sev == 'HIGH' else ("rule-card-med" if sev == 'MEDIUM' else "rule-card-low")
                    st.markdown(f"""
                    <div class="rule-card {card_cls}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #FFFFFF; font-size: 0.95rem;">{w.get('rule')}</strong>
                            <span style="font-size: 0.72rem; font-family: monospace; color: #00F0FF; background: rgba(0,240,255,0.1); padding: 2px 6px; border-radius: 4px;">{sev}</span>
                        </div>
                        <div style="font-family: monospace; font-size: 0.82rem; color: #00E5A3; margin: 6px 0;">
                            {w.get('values')}
                        </div>
                        <div style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 6px;">
                            <strong>Why Noteworthy:</strong> {w.get('explanation')}
                        </div>
                        <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 8px;">
                            <strong>Innocent Rationale:</strong> {w.get('legitimate_explanations')}
                        </div>
                        <div style="background: rgba(0, 240, 255, 0.05); padding: 8px; border-radius: 4px; font-size: 0.78rem; color: #E2E8F0; white-space: pre-line;">
                            <strong>Auditor Checklist:</strong>
                            {w.get('follow_up')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with row_c2:
            st.markdown("##### Analytical Scoring Deconstruction")
            if_sc = selected_period_row.get('unsupervised_anomaly_score', 0.0)
            if_fl = selected_period_row.get('unsupervised_anomaly_flag', 0)
            rf_pr = selected_period_row.get('supervised_probability', 0.0)
            rf_pr_label = selected_period_row.get('supervised_prediction', 0)
            rul_sc = selected_period_row.get('rules_score', 0.0)
            comp_sc = selected_period_row.get('composite_risk_score', 0.0)

            st.markdown(f"""
            <div style="background: #0B132B; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 18px;">
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
                        <span>Isolation Forest Anomaly Score (Weight 35%):</span>
                        <strong style="color: #00F0FF;">{if_sc:.1f} / 100 ({'FLAGGED OUTLIER' if if_fl == 1 else 'NORMAL'})</strong>
                    </div>
                    <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px;">
                        <div style="height: 6px; width: {min(if_sc, 100.0)}%; background: #00F0FF; border-radius: 3px;"></div>
                    </div>
                </div>
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
                        <span>Supervised Model Likelihood (Weight 35%):</span>
                        <strong style="color: #00E5A3;">{rf_pr:.1f}% ({'HIGH RISK PATTERN' if rf_pr_label == 1 else 'STANDARD'})</strong>
                    </div>
                    <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px;">
                        <div style="height: 6px; width: {min(rf_pr, 100.0)}%; background: #00E5A3; border-radius: 3px;"></div>
                    </div>
                </div>
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
                        <span>Forensic Heuristic Rules Score (Weight 30%):</span>
                        <strong style="color: #FFB800;">{rul_sc:.1f} / 100</strong>
                    </div>
                    <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px;">
                        <div style="height: 6px; width: {min(rul_sc, 100.0)}%; background: #FFB800; border-radius: 3px;"></div>
                    </div>
                </div>
                <div style="padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #FFFFFF;">Composite Surveillance Score:</span>
                    <span style="font-size: 1.5rem; font-weight: 800; font-family: monospace; color: #00F0FF;">{comp_sc:.1f} / 100</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### Core Financial Statement Metrics")
            fin_metrics = {
                'Revenue': f"{selected_period_row.get('revenue', 0):,.0f}",
                'Net Income': f"{selected_period_row.get('net_income', 0):,.0f}",
                'Operating Cash Flow': f"{selected_period_row.get('operating_cash_flow', 0):,.0f}",
                'Trade Receivables': f"{selected_period_row.get('receivables', 0):,.0f}",
                'Total Assets': f"{selected_period_row.get('assets', 0):,.0f}",
                'Total Debt': f"{selected_period_row.get('debt', 0):,.0f}"
            }
            fin_df = pd.DataFrame(list(fin_metrics.items()), columns=['Financial Indicator', 'Value'])
            st.table(fin_df)

# =============================================================================
# SECTION 3: UPLOAD & ANALYZE
# =============================================================================
elif nav_section == "3. Upload & Analyze":
    st.markdown("### Upload & Analyze Financial Data")
    st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 20px; font-size: 0.9rem;'>Ingest corporate financial CSV datasets or test single-company filings through the manual entry terminal.</div>", unsafe_allow_html=True)

    upload_tabs = st.tabs(["📁 Bulk CSV Upload & Batch Analysis", "✍️ Single-Company Manual Entry Terminal"])

    # Tab 1: CSV Upload
    with upload_tabs[0]:
        st.markdown("##### Batch Financial Dataset Verification")
        
        # Download Template button
        tmpl_df = generate_csv_template()
        csv_buf = io.StringIO()
        tmpl_df.to_csv(csv_buf, index=False)
        st.download_button(
            label="📥 Download Standard CSV Schema Template",
            data=csv_buf.getvalue(),
            file_name="corpshield_financial_template.csv",
            mime="text/csv"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload corporate financial CSV (supports multi-period data)", type=['csv'])

        if uploaded_file is not None:
            try:
                user_df = pd.read_csv(uploaded_file)
                is_valid, val_errors, val_meta = validate_uploaded_data(user_df)

                if not is_valid:
                    st.error("❌ Dataset Schema Validation Failed:")
                    for err in val_errors:
                        st.markdown(f"- {err}")
                else:
                    st.success(f"✓ Dataset verified successfully! Discovered {val_meta['unique_companies']} unique companies across {val_meta['total_rows']} period entries. Completeness: {val_meta['completeness_score']}%.")
                    if val_meta.get('warnings'):
                        with st.expander("Validation Advisory Notes"):
                            for w in val_meta['warnings']:
                                st.write(f"- {w}")

                    st.markdown("##### Upload Preview")
                    st.dataframe(user_df.head(10), use_container_width=True)

                    if st.button("🚀 Run Full CorpShield Forensic Surveillance Pipeline", type="primary"):
                        with st.spinner("Processing engineered financial features and executing ML inference..."):
                            analyzed_custom = analyzer.analyze(user_df)
                            st.session_state['current_df'] = analyzed_custom
                            st.session_state['data_source_mode'] = "Uploaded Custom Dataset"
                            st.success("Analysis complete! Dataset loaded into active surveillance session.")
                            st.rerun()

            except Exception as e:
                st.error(f"Error reading uploaded CSV: {e}")

    # Tab 2: Manual Entry Form
    with upload_tabs[1]:
        st.markdown("##### Manual Filing Entry Terminal")
        st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 15px; font-size: 0.82rem;'>Evaluate an individual company filing by providing current and prior period balance sheet and income statement numbers.</div>", unsafe_allow_html=True)

        with st.form("manual_entry_form"):
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown("<strong style='color: #00F0FF;'>Current Period Financials</strong>", unsafe_allow_html=True)
                m_name = st.text_input("Company Name", "Apex Dynamics Trial")
                m_period = st.text_input("Reporting Period", "FY2024")
                m_rev = st.number_input("Revenue", min_value=0.0, value=2500000000.0, step=1000000.0)
                m_ni = st.number_input("Net Income (Profit/Loss)", value=280000000.0, step=1000000.0)
                m_ocf = st.number_input("Operating Cash Flow", value=-50000000.0, step=1000000.0)
                m_rec = st.number_input("Trade Receivables", min_value=0.0, value=480000000.0, step=1000000.0)
                m_assets = st.number_input("Total Assets", min_value=1.0, value=4200000000.0, step=1000000.0)
                m_debt = st.number_input("Total Debt", min_value=0.0, value=1200000000.0, step=1000000.0)
                m_liab = st.number_input("Total Liabilities", min_value=0.0, value=1900000000.0, step=1000000.0)
                m_sector = st.selectbox("Sector", [
                    "Information Technology", "Pharmaceuticals & Healthcare", "Infrastructure & Capital Goods",
                    "Consumer Goods & Retail", "Automotive & Industrial", "Chemicals & Specialty Materials"
                ])

            with col_m2:
                st.markdown("<strong style='color: #00E5A3;'>Prior Period Historical Baseline</strong>", unsafe_allow_html=True)
                m_prev_period = st.text_input("Prior Reporting Period", "FY2023")
                m_prev_rev = st.number_input("Prior Period Revenue", min_value=0.0, value=2100000000.0, step=1000000.0)
                m_prev_ni = st.number_input("Prior Period Net Income", value=240000000.0, step=1000000.0)
                m_prev_ocf = st.number_input("Prior Period Operating Cash Flow", value=220000000.0, step=1000000.0)
                m_prev_rec = st.number_input("Prior Period Receivables", min_value=0.0, value=280000000.0, step=1000000.0)
                m_prev_debt = st.number_input("Prior Period Debt", min_value=0.0, value=900000000.0, step=1000000.0)
                m_prev_assets = st.number_input("Prior Period Total Assets", min_value=1.0, value=3800000000.0, step=1000000.0)
                m_rpt = st.number_input("Related-Party Transactions (Current)", min_value=0.0, value=0.0, step=100000.0)
                m_auditor_note = st.text_area("Auditor Remarks / Notes to Accounts", "Standard independent audit disclosures.")

            submit_manual = st.form_submit_button("⚡ Evaluate Manual Filing Now", type="primary")

        if submit_manual:
            manual_df = pd.DataFrame([{
                'company_id': 9999,
                'company_name': m_name,
                'period': m_period,
                'revenue': m_rev,
                'net_income': m_ni,
                'operating_cash_flow': m_ocf,
                'assets': m_assets,
                'liabilities': m_liab,
                'debt': m_debt,
                'receivables': m_rec,
                'prev_revenue': m_prev_rev,
                'prev_net_income': m_prev_ni,
                'prev_ocf': m_prev_ocf,
                'prev_receivables': m_prev_rec,
                'prev_debt': m_prev_debt,
                'prev_assets': m_prev_assets,
                'related_party_transactions': m_rpt,
                'sector': m_sector,
                'auditor_remarks': m_auditor_note,
                'data_source': "Manual Terminal Input",
                'is_synthetic': False
            }])

            analyzed_m = analyzer.analyze(manual_df)
            res_row = analyzed_m.iloc[0]

            st.markdown("#### Evaluation Results")
            r_col1, r_col2, r_col3 = st.columns(3)
            with r_col1:
                st.metric("Composite Screening Score", f"{res_row['composite_risk_score']:.1f} / 100")
            with r_col2:
                st.metric("Review Priority Tier", res_row['review_priority'])
            with r_col3:
                st.metric("Triggered Warning Rules", len(res_row['warnings']))

            if res_row['warnings']:
                st.markdown("##### Triggered Warning Rules:")
                for w in res_row['warnings']:
                    st.warning(f"**{w['rule']}** ({w['severity']})\n\n{w['explanation']}\n\n*Values:* {w['values']}")
            else:
                st.success("No anomalous warning rules triggered for this manual filing.")

# =============================================================================
# SECTION 4: AI MODEL LABORATORY
# =============================================================================
elif nav_section == "4. AI Model Laboratory":
    st.markdown("### AI Model Laboratory & Transparency Deck")
    st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 20px; font-size: 0.9rem;'>Rigorous machine-learning architecture documentation, feature importance rankings, and dynamic retraining controls.</div>", unsafe_allow_html=True)

    eval_json_path = 'reports/model_evaluation.json'
    eval_data = {}
    if os.path.exists(eval_json_path):
        with open(eval_json_path, 'r') as f:
            eval_data = json.load(f)

    # Top Model Specs
    spec_col1, spec_col2 = st.columns(2)
    with spec_col1:
        st.markdown("""
        <div class="cyber-metric-card">
            <div style="font-weight: 700; color: #00F0FF; font-size: 1.1rem; margin-bottom: 8px;">1. Unsupervised Anomaly Engine (Isolation Forest)</div>
            <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.5;">
                <strong>Role:</strong> Outlier detection across multi-dimensional financial ratios.<br>
                <strong>Estimators:</strong> 150 Isolation Trees (iTrees)<br>
                <strong>Contamination Factor:</strong> 0.10 (Calibrated for ~10% statistical outlier density)<br>
                <strong>Preprocessing:</strong> Robust Median Imputation + Standard Scaling<br>
                <strong>Ground-Truth Requirement:</strong> None. Operates completely independently of fraud labels.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with spec_col2:
        st.markdown("""
        <div class="cyber-metric-card">
            <div style="font-weight: 700; color: #00E5A3; font-size: 1.1rem; margin-bottom: 8px;">2. Supervised Pattern Classifier (Random Forest)</div>
            <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.5;">
                <strong>Role:</strong> Classifies complex non-linear combinations of forensic indicators.<br>
                <strong>Estimators:</strong> 120 Decision Trees with balanced class weights<br>
                <strong>Validation Strategy:</strong> GroupShuffleSplit (Entity-wise partition, zero temporal leakage)<br>
                <strong>Simulated Training Scope:</strong> Tested against deliberate synthetic accounting anomalies.<br>
                <strong>Crucial Note:</strong> Simulates patterns; does not assert real-world fraud conviction.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Evaluation Metrics
    if eval_data:
        st.markdown("##### Model Validation Metrics (Group-Wise Partitioning)")
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric("Precision", f"{eval_data.get('precision', 0.0):.3f}")
        with m2:
            st.metric("Recall", f"{eval_data.get('recall', 0.0):.3f}")
        with m3:
            st.metric("F1-Score", f"{eval_data.get('f1_score', 0.0):.3f}")
        with m4:
            st.metric("ROC-AUC", f"{eval_data.get('roc_auc', 0.0):.3f}")
        with m5:
            st.metric("PR-AUC", f"{eval_data.get('pr_auc', 0.0):.3f}")

        # Confusion Matrix Heatmap
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown("##### Confusion Matrix")
            cm = eval_data.get('confusion_matrix', [[0, 0], [0, 0]])
            cm_df = pd.DataFrame(cm, index=['Normal Records', 'Anomalous Records'], columns=['Pred Normal', 'Pred Anomaly'])
            fig_cm = px.imshow(
                cm_df,
                text_auto=True,
                color_continuous_scale=['#0B132B', '#00F0FF'],
                title="Confusion Matrix on Unseen Test Companies"
            )
            fig_cm.update_layout(get_plot_layout())
            st.plotly_chart(fig_cm, use_container_width=True)

        with c_right:
            st.markdown("##### Random Forest Feature Importance")
            importances = eval_data.get('feature_importances', {})
            if importances:
                imp_df = pd.DataFrame(list(importances.items()), columns=['Feature', 'Importance'])
                imp_df = imp_df.sort_values('Importance', ascending=True)
                fig_imp = px.bar(
                    imp_df,
                    x='Importance',
                    y='Feature',
                    orientation='h',
                    color='Importance',
                    color_continuous_scale=['#00E5A3', '#00F0FF'],
                    title="Predictive Weights of Engineered Forensic Metrics"
                )
                fig_imp.update_layout(get_plot_layout())
                st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature Dictionary
    st.markdown("##### Forensic Feature Dictionary & Methodology")
    dict_rows = []
    for f_key, f_meta in FEATURE_DEFINITIONS.items():
        dict_rows.append({
            'Feature Identifier': f_key,
            'Name': f_meta['name'],
            'Formula': f_meta['formula'],
            'Forensic Significance': f_meta['forensic_context']
        })
    dict_df = pd.DataFrame(dict_rows)
    st.dataframe(dict_df, use_container_width=True, height=260)

    st.markdown("<br>", unsafe_allow_html=True)

    # Live Retraining Controls
    st.markdown("##### Live Model Retraining Pipeline")
    st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 15px; font-size: 0.85rem;'>Genuinely retrains the Isolation Forest and Random Forest pipelines on the currently loaded dataset. Updates model weights and evaluation metrics.</div>", unsafe_allow_html=True)

    col_btn, col_msg = st.columns([1, 2])
    with col_btn:
        if st.button("⚡ Retrain Models on Active Cohort", type="primary"):
            with st.spinner("Retraining Isolation Forest and Random Forest with GroupShuffleSplit..."):
                retrained_metrics = train_and_evaluate_models(st.session_state['current_df'])
                st.cache_resource.clear()
                st.success(f"Models retrained successfully at {datetime.now().strftime('%H:%M:%S')}! New artifacts saved to models/ directory.")
                st.rerun()

# =============================================================================
# SECTION 5: FINANCIAL REPORTS
# =============================================================================
elif nav_section == "5. Financial Reports":
    st.markdown("### Forensic Financial Reports & Export Terminal")
    st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 20px; font-size: 0.9rem;'>Generate comprehensive, publication-ready surveillance dossiers for individual entities or export the analyzed cohort.</div>", unsafe_allow_html=True)

    rep_c1, rep_c2 = st.columns([1, 1])

    with rep_c1:
        st.markdown("##### Company Surveillance Intelligence Dossier")
        rep_company = st.selectbox("Select Target Entity", sorted(df['company_name'].unique().tolist()))
        company_records = df[df['company_name'] == rep_company].sort_values('period')
        latest_record = company_records.iloc[-1]

        # Generate HTML Dossier
        html_report = generate_company_html_dossier(latest_record, company_records, FEATURE_DEFINITIONS)

        st.markdown(f"""
        <div style="background: #0B132B; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 16px; margin: 15px 0;">
            <div style="font-weight: 700; color: #00F0FF; font-size: 1.1rem;">{rep_company}</div>
            <div style="font-size: 0.85rem; color: #CBD5E1; margin: 4px 0;">
                Latest Period: <strong>{latest_record.get('period', 'N/A')}</strong> | Priority: <strong>{latest_record.get('review_priority', 'LOW')}</strong>
            </div>
            <div style="font-size: 0.82rem; color: #94A3B8;">
                Triggered Warning Rules: <strong>{len(latest_record.get('warnings', []))}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            label="📄 Download Formatted HTML Dossier (Printable / Save-as-PDF)",
            data=html_report,
            file_name=f"corpshield_dossier_{rep_company.replace(' ', '_')}.html",
            mime="text/html"
        )

    with rep_c2:
        st.markdown("##### Cohort Analytical Data Export")
        st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 15px; font-size: 0.85rem;'>Export the complete analyzed dataset including calculated ratios, ML anomaly scores, flags, and rule summaries in CSV format.</div>", unsafe_allow_html=True)

        export_df = df.copy()
        # Clean warnings column for clean CSV export
        if 'warnings' in export_df.columns:
            export_df['warnings_export'] = ["; ".join([w['rule'] for w in wl]) if wl else "None" for wl in export_df['warnings']]
            export_df_clean = export_df.drop(columns=['warnings'])
        else:
            export_df_clean = export_df

        csv_exp = io.StringIO()
        export_df_clean.to_csv(csv_exp, index=False)

        st.download_button(
            label="📊 Download Full Analyzed Cohort Dataset (CSV)",
            data=csv_exp.getvalue(),
            file_name="corpshield_analyzed_cohort.csv",
            mime="text/csv"
        )

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
    st.markdown("##### Dossier Live Visual Preview")
    with st.expander("👁️ Open Full In-Browser Dossier Preview", expanded=False):
        st.components.v1.html(html_report, height=750, scrolling=True)

# =============================================================================
# SECTION 6: DATA SOURCES & METHODOLOGY
# =============================================================================
elif nav_section == "6. Data Sources & Methodology":
    st.markdown("### Data Sources & Surveillance Methodology")
    st.markdown("<div style='color: #94A3B8; margin-top: -8px; margin-bottom: 20px; font-size: 0.9rem;'>Academic provenance, SEBI investor-protection principles, and scoring methodology transparency.</div>", unsafe_allow_html=True)

    st.markdown(r"""
    #### 1. SEBI Investor-Protection Alignment
    The Securities and Exchange Board of India (SEBI) places significant emphasis on proactive market surveillance, 
    forensic accounting scrutiny, and early identification of corporate disclosures that mask underlying business realities.
    
    CorpShield AI is designed as a **student research surveillance prototype** that incorporates the forensic accounting principles 
    advocated by forensic auditors and regulatory analysts:
    - **Cash-to-Earnings Integrity:** Verifying whether top-line growth translates into genuine operational cash flow.
    - **Channel Stuffing Surveillance:** Detecting fictitious or premature invoicing where trade receivables outpace revenue.
    - **Leverage Camouflage:** Identifying rapid borrowing surges accompanied by deteriorating operational profitability.
    - **Sloan's Accrual Anomaly:** Monitoring balance-sheet accruals relative to total assets.

    #### 2. Composite Screening Score Formula
    The composite risk score ($S_{composite} \in [0, 100]$) is computed through a transparent weighted architecture:
    """)
    st.latex(r"S_{composite} = 0.35 \times S_{IF} + 0.35 \times P_{RF} + 0.30 \times S_{Rules}")
    st.markdown(r"""
    - $S_{IF}$: Normalized Isolation Forest outlier score ($0-100$).
    - $P_{RF}$: Supervised Random Forest probability of simulated anomaly match ($0-100\%$).
    - $S_{Rules}$: Aggregate weight of triggered heuristic forensic rules clamped at $100$.

    **Review Priority Tiers:**
    - **HIGH PRIORITY:** $S_{composite} \ge 65.0$ or $\ge 3$ critical forensic rules triggered. Demands immediate investigator attention.
    - **MODERATE PRIORITY:** $S_{composite} \in [35.0, 64.9]$ or $\ge 1$ forensic rule triggered. Watchlist classification.
    - **LOW PRIORITY:** $S_{composite} < 35.0$. Conforms to standard operational baseline.

    #### 3. Data Provenance & Honest Machine-Learning Disclosure
    - **Synthetic Research Dataset:** In the absence of a comprehensive, publicly available, machine-readable dataset of verified real-world corporate fraud convictions with uniform period reporting, the primary dataset is generated via a reproducible stochastic simulation (`n_companies=120`, `periods=6`, `random_seed=42`).
    - **Public Listed Disclosures:** Includes audited public annual report numbers for prominent enterprises (e.g. Apple, Microsoft, Tesla, Amazon, Alphabet).
    - **Strict Principle of Honest Attribution:** An anomaly detected by machine learning or a heuristic rule **never** constitutes proof of fraud or wrongdoing. Genuine listed enterprises often exhibit cash-flow divergences during legitimate capital expansion phases.
    """)

# -----------------------------------------------------------------------------
# 5. FOOTER DISCLAIMER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="sebi-disclaimer-card">
    <strong>SURVEILLANCE SCREENING DISCLAIMER:</strong><br>
    CorpShield AI is an academic research and student screening prototype for corporate financial anomaly detection. 
    Its predictions and risk scores are not proof of fraud, an investment recommendation, or an official SEBI assessment. 
    Results flag statistical deviations for investigator review and require independent verification against certified statutory filings.
</div>
""", unsafe_allow_html=True)
