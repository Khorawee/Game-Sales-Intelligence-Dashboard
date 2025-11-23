# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Game Sales Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 45px;
        padding: 10px;
        background: linear-gradient(90deg, #00f5d4, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(-15px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .glass-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-8px);
    }
</style>
""", unsafe_allow_html=True)


# Database Connection
@st.cache_data
def load_data():
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "game_sales")

    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
    query = """
        SELECT v.game_name AS Name, p.name AS Platform, g.name AS Genre,
               pub.name AS Publisher, v.Year, v.NA_Sales, v.EU_Sales, 
               v.JP_Sales, v.Other_Sales, v.Global_Sales
        FROM vgsales v
        JOIN platform p ON v.platform_id = p.id
        JOIN genre g ON v.genre_id = g.id
        JOIN publisher pub ON v.publisher_id = pub.id
    """
    return pd.read_sql(query, engine)

df = load_data()

# Sidebar Filters
st.sidebar.title("📊 Dashboard Controls")
st.sidebar.image(
    "https://static.vecteezy.com/system/resources/thumbnails/019/900/476/small/game-controller-icon-illustration-video-game-controller-free-vector.jpg",
    width="stretch"  # ✅ ใช้แทน use_container_width=True
)
selected_platform = st.sidebar.multiselect("🎮 Filter by Platform", df["Platform"].unique())
selected_genre = st.sidebar.multiselect("🎭 Filter by Genre", df["Genre"].unique())

if selected_platform:
    df = df[df["Platform"].isin(selected_platform)]
if selected_genre:
    df = df[df["Genre"].isin(selected_genre)]

st.sidebar.info("💡 Tip: Click on graphs to view fullscreen")

# Main Title
st.markdown('<h1 class="main-title">🎮 Game Sales Analytics Dashboard</h1>', unsafe_allow_html=True)

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='glass-card'>🎮<br>Total Games<br><b>{len(df):,}</b></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='glass-card'>💰<br>Total Sales<br><b>{df['Global_Sales'].sum():.2f}M</b></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='glass-card'>🕹️<br>Platforms<br><b>{df['Platform'].nunique()}</b></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='glass-card'>🎭<br>Genres<br><b>{df['Genre'].nunique()}</b></div>", unsafe_allow_html=True)


# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏆 Rankings", "🌍 Regions", "🔥 Analysis"])

# TAB 1: Trends
with tab1:
    st.subheader("📈 Global Sales Over Time")
    ts = df[df['Year'] > 1980].groupby("Year")['Global_Sales'].sum().reset_index()
    fig = px.line(ts, x='Year', y='Global_Sales', template="plotly_dark", markers=True)
    fig.update_layout(height=450, margin=dict(l=50, r=50, t=50, b=50))
    st.plotly_chart(fig, use_container_width=True)


# TAB 2: Rankings
with tab2:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🏢 Top Publishers")
        top_pub = df.groupby("Publisher")["Global_Sales"].sum().nlargest(10).reset_index()
        fig = px.bar(top_pub, x="Global_Sales", y="Publisher", orientation='h', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎭 Top Genres")
        top_genre = df.groupby("Genre")["Global_Sales"].sum().nlargest(10).reset_index()
        fig = px.bar(top_genre, x="Global_Sales", y="Genre", orientation='h', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("### 🎮 Top Games")
        top_games = df.nlargest(10, 'Global_Sales')[['Name', 'Global_Sales']]
        fig = px.bar(top_games, x="Global_Sales", y="Name", orientation='h', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)


# TAB 3: Regional Sales
with tab3:
    st.subheader("🌎 Regional Sales Distribution")
    regions = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
    vals = [df[col].sum() for col in regions]

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = go.Figure(go.Bar(
            x=regions,
            y=vals,
            text=[f"{v:.2f}M" for v in vals],
            textposition='outside',
            textfont=dict(size=16, color='white', family='Arial'),
            marker_color=['#7DA6FF', '#FF8C75', '#46D18A', '#B37DFF']
        ))

        fig.update_layout(
            template="plotly_dark",
            height=450,
            yaxis_title="Sales (Million Units)",
            margin=dict(t=60, l=40, r=40, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            values=vals, 
            names=regions, 
            hole=0.4, 
            template="plotly_dark",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF']  # สีสดใส ดูง่ายขึ้น
        )
        fig.update_traces(
            textposition='inside',
            textfont_size=14,
            marker=dict(line=dict(color='#1a1a1a', width=2))  # เส้นขอบชัดเจน
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)


# TAB 4: Heatmap
with tab4:
    st.subheader("🔥 Platform × Genre Heatmap")

    pivot = df.pivot_table(values="Global_Sales", index="Genre", columns="Platform",
                           aggfunc="sum", fill_value=0)
    pivot = pivot.loc[pivot.sum(axis=1).nlargest(10).index,
                      pivot.sum(axis=0).nlargest(12).index]

    fig = px.imshow(
        pivot,
        text_auto=True,
        template='plotly_dark',
        aspect='auto',
    )

    fig.update_layout(
        width=None,
        height=800,
        margin=dict(l=80, r=80, t=80, b=80),
        coloraxis_colorbar=dict(title="Sales (M)", tickfont=dict(size=14))
    )

    fig.update_xaxes(side="top", tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>✨ Developed by Streamlit + Plotly</div>", unsafe_allow_html=True)