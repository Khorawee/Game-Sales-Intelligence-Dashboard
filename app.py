# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import joblib
from preprocessor import FullPreprocessor

load_dotenv()

st.set_page_config(page_title="Game Sales Dashboard", layout="wide")

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 45px;
        padding: 10px;
        background: linear-gradient(90deg, #00f5d4, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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

@st.cache_data
def load_data():
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "game_sales")
    
    # Check if password exists to avoid connection errors
    if not DB_PASSWORD:
        st.error("Error: DB_PASSWORD not found in .env file")
        return pd.DataFrame()

    try:
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
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return pd.DataFrame()

@st.cache_resource
def load_ml_model():
    try:
        model = joblib.load("models/model_xgb.pkl")
        preprocessor = joblib.load("models/preprocessor.pkl")
        return model, preprocessor
    except:
        return None, None

df = load_data()
model, preprocessor = load_ml_model()

st.sidebar.title("Dashboard Controls")

# Sidebar Filters
if not df.empty:
    selected_platform = st.sidebar.multiselect("Filter by Platform", sorted(df["Platform"].unique()))
    selected_genre = st.sidebar.multiselect("Filter by Genre", sorted(df["Genre"].unique()))

    df_filtered = df.copy()
    if selected_platform:
        df_filtered = df_filtered[df_filtered["Platform"].isin(selected_platform)]
    if selected_genre:
        df_filtered = df_filtered[df_filtered["Genre"].isin(selected_genre)]
else:
    df_filtered = pd.DataFrame()
    st.warning("No data available. Please check your database connection.")

st.sidebar.info("Tip: Click on graphs to view fullscreen")

st.markdown('<h1 class="main-title">Game Sales Analytics Dashboard</h1>', unsafe_allow_html=True)

# KPI Cards
if not df_filtered.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"<div class='glass-card'>Total Games<br><b>{len(df_filtered):,}</b></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='glass-card'>Total Sales<br><b>{df_filtered['Global_Sales'].sum():.2f}M</b></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='glass-card'>Platforms<br><b>{df_filtered['Platform'].nunique()}</b></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='glass-card'>Genres<br><b>{df_filtered['Genre'].nunique()}</b></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Trends", "Rankings", "Regions", "Heatmap", "Correlations", "ML Prediction"])

    with tab1:
        st.subheader("Global Sales Over Time")
        ts = df_filtered[df_filtered['Year'] > 1980].groupby("Year")['Global_Sales'].sum().reset_index()
        fig = px.line(ts, x='Year', y='Global_Sales', template="plotly_dark", markers=True)
        fig.update_traces(line_color='#00f5d4', line_width=3)
        fig.update_layout(height=450, margin=dict(l=50, r=50, t=50, b=50))
        st.plotly_chart(fig, width="stretch")

    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### Top Publishers")
            top_pub = df_filtered.groupby("Publisher")["Global_Sales"].sum().nlargest(10).reset_index()
            fig = px.bar(top_pub, x="Global_Sales", y="Publisher", orientation='h', template='plotly_dark')
            st.plotly_chart(fig, width="stretch")
        with col2:
            st.markdown("### Top Genres")
            top_genre = df_filtered.groupby("Genre")["Global_Sales"].sum().nlargest(10).reset_index()
            fig = px.bar(top_genre, x="Global_Sales", y="Genre", orientation='h', template='plotly_dark')
            st.plotly_chart(fig, width="stretch")
        with col3:
            st.markdown("### Top Games")
            top_games = df_filtered.nlargest(10, 'Global_Sales')[['Name', 'Global_Sales']]
            fig = px.bar(top_games, x="Global_Sales", y="Name", orientation='h', template='plotly_dark')
            st.plotly_chart(fig, width="stretch")

    with tab3:
        st.subheader("Regional Sales Distribution")
        regions = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
        vals = [df_filtered[col].sum() for col in regions]
        region_names = ["North America", "Europe", "Japan", "Other Regions"]
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = go.Figure(go.Bar(x=region_names, y=vals, text=[f"{v:.2f}M" for v in vals], textposition='outside',
                                   marker_color=['#7DA6FF', '#FF8C75', '#46D18A', '#B37DFF']))
            fig.update_layout(template="plotly_dark", height=450, yaxis_title="Sales (Million Units)")
            st.plotly_chart(fig, width="stretch")
        with col2:
            fig = px.pie(values=vals, names=region_names, hole=0.4, template="plotly_dark")
            fig.update_layout(height=450)
            st.plotly_chart(fig, width="stretch")

    with tab4:
        st.subheader("Platform x Genre Heatmap")
        pivot = df_filtered.pivot_table(values="Global_Sales", index="Genre", columns="Platform", aggfunc="sum", fill_value=0)
        # Select top 12 platforms and top 10 genres to keep heatmap readable
        top_platforms = pivot.sum(axis=0).nlargest(12).index
        top_genres = pivot.sum(axis=1).nlargest(10).index
        pivot = pivot.loc[top_genres, top_platforms]
        
        fig = px.imshow(pivot, text_auto='.1f', template='plotly_dark', aspect='auto')
        fig.update_layout(height=700)
        st.plotly_chart(fig, width="stretch")

    with tab5:
        st.subheader("Feature Correlation Analysis")
        numeric_cols = ['Year', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
        corr_matrix = df_filtered[numeric_cols].corr()
        fig = px.imshow(corr_matrix, text_auto='.3f', aspect='auto', color_continuous_scale='RdBu_r', 
                        template='plotly_dark', zmin=-1, zmax=1)
        fig.update_layout(height=600)
        st.plotly_chart(fig, width="stretch")

    with tab6:
        st.subheader("ML Prediction")
        if model is None:
            st.error("ML Model not found. Please run `train_model.py` first to generate models.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                pred_platform = st.selectbox("Platform", sorted(df["Platform"].unique()))
                pred_genre = st.selectbox("Genre", sorted(df["Genre"].unique()))
            with col2:
                pred_publisher = st.selectbox("Publisher", sorted(df["Publisher"].unique()))
                pred_year = st.number_input("Year", 1980, 2030, 2024)
            with col3:
                pred_na = st.number_input("NA Sales (M)", 0.0, 100.0, 1.0, 0.1)
                pred_eu = st.number_input("EU Sales (M)", 0.0, 100.0, 0.5, 0.1)
            pred_jp = st.number_input("JP Sales (M)", 0.0, 100.0, 0.3, 0.1)
            pred_other = st.number_input("Other Sales (M)", 0.0, 100.0, 0.2, 0.1)
            
            if st.button("Predict", type="primary"):
                # 1. Total Known Sales
                total_known_sales = pred_na + pred_eu + pred_jp + pred_other
                
                # 2. Publisher Avg (Get historical average from loaded dataframe)
                publisher_stats = df[df['Publisher'] == pred_publisher]['Global_Sales']
                if not publisher_stats.empty:
                    publisher_avg = publisher_stats.mean()
                else:
                    publisher_avg = 0.0 # Default if new publisher
                
                # 3. Platform Count (Get historical count from loaded dataframe)
                platform_stats = df[df['Platform'] == pred_platform]
                platform_count = platform_stats.shape[0] if not platform_stats.empty else 0

                # Create DataFrame with ALL features expected by the model
                input_data = pd.DataFrame([{
                    'Name': 'Prediction', 
                    'Platform': pred_platform, 
                    'Genre': pred_genre,
                    'Publisher': pred_publisher, 
                    'Year': pred_year, 
                    'NA_Sales': pred_na,
                    'EU_Sales': pred_eu, 
                    'JP_Sales': pred_jp, 
                    'Other_Sales': pred_other,
                    # Added features
                    'Total_Known_Sales': total_known_sales,
                    'Publisher_Avg': publisher_avg,
                    'Platform_Count': platform_count
                }])

                try:
                    processed = preprocessor.transform(input_data)
                    # Convert to standard Python float to avoid float32 errors in Streamlit
                    prediction = float(model.predict(processed)[0])
                    
                    st.success(f"Predicted Global Sales: **{prediction:.2f}M Units**")
                    
                    col_a, col_b = st.columns(2)
                    col_a.metric("Input Total (Regions)", f"{total_known_sales:.2f}M")
                    col_b.metric("AI Prediction (Global)", f"{prediction:.2f}M")
                    
                    # Convert to standard Python float for the progress bar
                    progress_val = min(prediction / 20.0, 1.0)
                    st.progress(float(progress_val))
                    
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
                    st.error("Please ensure the input data format matches the training data.")

st.markdown("---")
st.markdown("<div style='text-align: center;'>Developed by Streamlit + Plotly + XGBoost</div>", unsafe_allow_html=True)