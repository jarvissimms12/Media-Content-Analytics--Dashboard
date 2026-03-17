"""
Media Content Analytics Dashboard
====================================
An interactive Streamlit dashboard analyzing content performance
across media categories — built to demonstrate BI Analyst skills
relevant to companies like Hearst Magazines and Share Local Media.

Author: Jarvis Simms
Tools:  Python, Streamlit, pandas, plotly, requests
Deploy: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import requests
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Media Content Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .metric-card .value { font-size: 2rem; font-weight: 700; }
    .metric-card .label { font-size: 0.85rem; opacity: 0.85; margin-top: 0.2rem; }
    .metric-card .delta { font-size: 0.8rem; margin-top: 0.3rem; }
    .section-header {
        border-left: 4px solid #1565C0;
        padding-left: 0.75rem;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1565C0;
    }
    [data-testid="stMetric"] { background: #f8f9fa; border-radius: 8px; padding: 0.75rem; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# DATA GENERATION — Realistic synthetic media analytics data
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 500
    categories = ["Lifestyle", "Technology", "Finance", "Health", "Entertainment", "Politics", "Sports"]
    sources = ["Website", "Newsletter", "Social Media", "Syndication", "Direct"]
    regions = ["Northeast", "Southeast", "Midwest", "West", "International"]

    dates = pd.date_range(end=datetime.today(), periods=n, freq="12h")

    df = pd.DataFrame({
        "date": dates,
        "category": np.random.choice(categories, n, p=[0.20, 0.18, 0.15, 0.14, 0.13, 0.11, 0.09]),
        "source": np.random.choice(sources, n, p=[0.35, 0.25, 0.22, 0.12, 0.06]),
        "region": np.random.choice(regions, n),
        "views": np.random.lognormal(mean=8.5, sigma=1.2, size=n).astype(int),
        "unique_visitors": np.random.lognormal(mean=7.8, sigma=1.1, size=n).astype(int),
        "avg_time_on_page_sec": np.random.normal(180, 60, n).clip(30, 600).astype(int),
        "scroll_depth_pct": np.random.beta(2, 2, n) * 100,
        "clicks": np.random.lognormal(mean=5.5, sigma=1.0, size=n).astype(int),
        "shares": np.random.lognormal(mean=3.5, sigma=1.2, size=n).astype(int),
        "revenue_usd": np.random.lognormal(mean=4.5, sigma=1.3, size=n).round(2),
    })

    # Add realistic correlations
    df["views"] = (df["views"] * np.where(df["category"] == "Technology", 1.3, 1.0)).astype(int)
    df["revenue_usd"] = (df["revenue_usd"] * np.where(df["source"] == "Newsletter", 1.4, 1.0)).round(2)
    df["engagement_rate"] = (df["clicks"] / df["views"] * 100).round(2)
    df["week"] = df["date"].dt.to_period("W").astype(str)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["day_of_week"] = df["date"].dt.day_name()

    return df


df = load_data()

# ══════════════════════════════════════════════════════════════
# SIDEBAR — Filters
# ══════════════════════════════════════════════════════════════
st.sidebar.image("https://img.shields.io/badge/Media%20Analytics-Dashboard-1565C0?style=for-the-badge", use_column_width=True)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Filters")

selected_categories = st.sidebar.multiselect(
    "Content Category",
    options=sorted(df["category"].unique()),
    default=sorted(df["category"].unique())
)

selected_sources = st.sidebar.multiselect(
    "Traffic Source",
    options=sorted(df["source"].unique()),
    default=sorted(df["source"].unique())
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(df["date"].min().date(), df["date"].max().date()),
    min_value=df["date"].min().date(),
    max_value=df["date"].max().date()
)

st.sidebar.markdown("---")
st.sidebar.markdown("**About this Dashboard**")
st.sidebar.caption(
    "Built by **Jarvis Simms** to demonstrate BI Analyst skills: "
    "data ingestion, KPI tracking, trend analysis, and interactive reporting. "
    "Tools: Python · Streamlit · Plotly · pandas"
)
st.sidebar.markdown("[GitHub](https://github.com/jarvissimms12)")

# ── Apply filters ──────────────────────────────────────────────
filtered = df[
    df["category"].isin(selected_categories) &
    df["source"].isin(selected_sources) &
    (df["date"].dt.date >= date_range[0]) &
    (df["date"].dt.date <= date_range[1])
].copy()

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("# 📊 Media Content Analytics Dashboard")
st.markdown(
    f"**{len(filtered):,} articles** across **{filtered['category'].nunique()} categories** "
    f"| {date_range[0]} → {date_range[1]} "
    f"| Built by Jarvis Simms"
)
st.markdown("---")

# ══════════════════════════════════════════════════════════════
# KPI METRICS ROW
# ══════════════════════════════════════════════════════════════
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_views = filtered["views"].sum()
    st.metric("Total Views", f"{total_views:,.0f}", delta=f"+12.3% vs prev period")

with col2:
    total_visitors = filtered["unique_visitors"].sum()
    st.metric("Unique Visitors", f"{total_visitors:,.0f}", delta="+8.7%")

with col3:
    avg_eng = filtered["engagement_rate"].mean()
    st.metric("Avg Engagement Rate", f"{avg_eng:.1f}%", delta="+1.2pp")

with col4:
    avg_time = filtered["avg_time_on_page_sec"].mean()
    st.metric("Avg Time on Page", f"{avg_time:.0f}s", delta="+15s")

with col5:
    total_rev = filtered["revenue_usd"].sum()
    st.metric("Total Revenue", f"${total_rev:,.0f}", delta="+$4,230")

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# ROW 1: Trend + Category Breakdown
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📈 Performance Trends</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    weekly = filtered.groupby("week").agg(
        views=("views", "sum"),
        revenue=("revenue_usd", "sum"),
        engagement=("engagement_rate", "mean")
    ).reset_index()

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(
        go.Scatter(x=weekly["week"], y=weekly["views"], name="Views",
                   line=dict(color="#1565C0", width=2.5),
                   fill="tozeroy", fillcolor="rgba(21,101,192,0.08)"),
        secondary_y=False
    )
    fig_trend.add_trace(
        go.Scatter(x=weekly["week"], y=weekly["revenue"], name="Revenue ($)",
                   line=dict(color="#FF6B35", width=2, dash="dot")),
        secondary_y=True
    )
    fig_trend.update_layout(
        title="Weekly Views vs Revenue", height=320,
        legend=dict(orientation="h", y=1.15),
        xaxis=dict(tickangle=30, nticks=10),
        margin=dict(t=50, b=60)
    )
    fig_trend.update_yaxes(title_text="Views", secondary_y=False)
    fig_trend.update_yaxes(title_text="Revenue ($)", secondary_y=True)
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    cat_perf = filtered.groupby("category").agg(
        views=("views", "sum"),
        revenue=("revenue_usd", "sum"),
        engagement=("engagement_rate", "mean")
    ).reset_index().sort_values("views", ascending=False)

    fig_cat = px.bar(
        cat_perf, x="views", y="category", orientation="h",
        color="engagement", color_continuous_scale="Blues",
        labels={"views": "Total Views", "category": "", "engagement": "Eng. Rate %"},
        title="Views by Category (color = engagement)"
    )
    fig_cat.update_layout(height=320, margin=dict(t=50, b=30), coloraxis_showscale=False)
    st.plotly_chart(fig_cat, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# ROW 2: Source Analysis + Day-of-Week + Scatter
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🔍 Audience & Source Deep Dive</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    src = filtered.groupby("source").agg(
        views=("views", "sum"),
        revenue=("revenue_usd", "sum")
    ).reset_index()
    fig_src = px.pie(src, values="views", names="source", hole=0.45,
                     title="Traffic Source Breakdown",
                     color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_src.update_layout(height=300, margin=dict(t=50, b=10))
    st.plotly_chart(fig_src, use_container_width=True)

with col2:
    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow = filtered.groupby("day_of_week")["views"].mean().reindex(dow_order).reset_index()
    fig_dow = px.bar(dow, x="day_of_week", y="views",
                     color="views", color_continuous_scale="Blues",
                     title="Avg Views by Day of Week",
                     labels={"day_of_week": "", "views": "Avg Views"})
    fig_dow.update_layout(height=300, margin=dict(t=50, b=30), coloraxis_showscale=False,
                          xaxis=dict(tickangle=30))
    st.plotly_chart(fig_dow, use_container_width=True)

with col3:
    fig_scatter = px.scatter(
        filtered.sample(min(200, len(filtered))),
        x="avg_time_on_page_sec", y="engagement_rate",
        color="category", size="views",
        title="Time on Page vs Engagement Rate",
        labels={"avg_time_on_page_sec": "Avg Time (sec)", "engagement_rate": "Engagement (%)"},
        opacity=0.7
    )
    fig_scatter.update_layout(height=300, margin=dict(t=50, b=30),
                               legend=dict(font=dict(size=9), title=""))
    st.plotly_chart(fig_scatter, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# ROW 3: Revenue Heatmap + Top Articles Table
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">💰 Revenue Intelligence & Top Performers</div>', unsafe_allow_html=True)

col_heat, col_table = st.columns([1, 1])

with col_heat:
    pivot = filtered.groupby(["category", "source"])["revenue_usd"].sum().unstack(fill_value=0)
    fig_heat = px.imshow(
        pivot, text_auto=".0f",
        color_continuous_scale="Blues",
        title="Revenue Heatmap: Category × Source ($)",
        labels=dict(x="Traffic Source", y="Category", color="Revenue")
    )
    fig_heat.update_layout(height=320, margin=dict(t=50, b=30))
    st.plotly_chart(fig_heat, use_container_width=True)

with col_table:
    st.markdown("**🏆 Top 10 Performing Articles (by Views)**")
    top10 = (
        filtered.nlargest(10, "views")[
            ["date", "category", "source", "views", "engagement_rate", "revenue_usd"]
        ]
        .assign(
            date=lambda x: x["date"].dt.strftime("%Y-%m-%d"),
            views=lambda x: x["views"].map("{:,}".format),
            revenue_usd=lambda x: x["revenue_usd"].map("${:,.2f}".format),
            engagement_rate=lambda x: x["engagement_rate"].map("{:.1f}%".format)
        )
        .rename(columns={
            "date": "Date", "category": "Category", "source": "Source",
            "views": "Views", "engagement_rate": "Eng. Rate", "revenue_usd": "Revenue"
        })
        .reset_index(drop=True)
    )
    top10.index += 1
    st.dataframe(top10, use_container_width=True, height=300)

# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("---")
st.caption(
    "📊 Media Content Analytics Dashboard · Built by **Jarvis Simms** · "
    "MS Data Science, NYIT 2025 · Tools: Python, Streamlit, Plotly, pandas · "
    "[GitHub](https://github.com/jarvissimms12)"
)
