# 🔮 ML Prediction Page
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from preprocessor import FullPreprocessor

# Load Model & Preprocessor
@st.cache_resource
def load_model():
    model = joblib.load("models/model.pkl")  # 👈 เปลี่ยนชื่อไฟล์โมเดลได้
    preprocessor = joblib.load("models/preprocessor.pkl")  # ถ้ามี
    return model, preprocessor

model, preprocessor = load_model()

# Page layout
st.title("🔮 Game Sales Prediction")
st.markdown("พยากรณ์ยอดขายเกม (Global Sales) โดยใช้ Machine Learning 🚀")

# Input form
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("🎮 Game Name")
    year = st.number_input("📆 Release Year", min_value=1980, max_value=2025, step=1)
    platform = st.selectbox("🕹️ Platform", ['PS2', 'X360', 'PS3', 'Wii', 'DS', 'GBA', 'PC', 'PS4', 'XB'])
    
with col2:
    genre = st.selectbox("🎭 Genre", ['Action', 'Sports', 'Shooter', 'Role-Playing', 'Platform', 'Simulation'])
    publisher = st.text_input("🏢 Publisher")
    na_sales = st.number_input("🇺🇸 NA Sales (M)", min_value=0.0, max_value=200.0, step=0.1)
    eu_sales = st.number_input("🇪🇺 EU Sales (M)", min_value=0.0, max_value=200.0, step=0.1)

jp_sales = st.number_input("🇯🇵 JP Sales (M)", min_value=0.0, max_value=200.0, step=0.1)
other_sales = st.number_input("🌍 Other Sales (M)", min_value=0.0, max_value=200.0, step=0.1)

# Prediction Button
if st.button("🚀 Predict Global Sales"):
    # Create DataFrame
    input_data = pd.DataFrame([{
        'Name': name,
        'Platform': platform,
        'Genre': genre,
        'Publisher': publisher,
        'Year': year,
        'NA_Sales': na_sales,
        'EU_Sales': eu_sales,
        'JP_Sales': jp_sales,
        'Other_Sales': other_sales
    }])

    try:
        processed = preprocessor.transform(input_data)
        prediction = model.predict(processed)[0]

        st.success(f"🎯 Predicted Global Sales: **{prediction:.2f} Million Units** 💰")

        st.metric(label="📈 Expected Sales", value=f"{prediction:.2f}M")
        
        st.progress(min(prediction / 100, 1))

    except Exception as e:
        st.error(f"Error processing input: {e}")

st.markdown("---")
st.info("💡 ML Model is trained using RandomForest / XGBoost on historical sales data.")
