# pages/1_Model_Trainer.py
import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_temperature_data
from utils.ML_model_dev import (
    multiple_linear_regression, ridge_regression, lasso_regression, gradient_boosting_regression
)

st.title("🌡️ Train Regression Models to Predict Temperature")

# Load and clean data
df = load_temperature_data()
df = df.select_dtypes(include=[np.number]).dropna()
#st.write("Available columns:", df.columns.tolist())

required_columns = {'Year', 'Month', 'Day'}
if not required_columns.issubset(df.columns):
    st.error("Dataset must include 'Year', 'Month', and 'Day' columns for prediction.")
    st.stop()

# Define features and target
target = 'Temp_2m'
if target not in df.columns:
    st.error(f"❌ Column `{target}` not found in dataset.")
    st.stop()

features = [col for col in df.columns if col != target]
X = df[features]
y = df[target]

# st.markdown(f"**Target Variable:** `{target}`")
# st.markdown(f"**Features Used for Training:** `{', '.join(features)}`")

# Model selection
model_choice = st.selectbox("📌 Select Regression Model", [
    "Multiple Linear Regression",
    "Ridge Regression",
    "Lasso Regression",
    "Gradient Boosting Regression"
])

model = None

# Train model
if st.button("🚀 Train Model"):
    if model_choice == "Multiple Linear Regression":
        model = multiple_linear_regression(X, y)
    elif model_choice == "Ridge Regression":
        model = ridge_regression(X, y)
    elif model_choice == "Lasso Regression":
        model = lasso_regression(X, y)
    elif model_choice == "Gradient Boosting Regression":
        model = gradient_boosting_regression(X, y)
    st.success("✅ Model trained successfully!")

# Prediction section
st.subheader("📅 Predict Temperature for Any Date")

Year = st.slider("Year", 2025, 2050, 2025)
Month = st.slider("Month", 1, 12, 1)
Day = st.slider("Day", 1, 31, 1)

if model:
    # Base input dict
    input_data = {
        'Year': Year,
        'Month': Month,
        'Day': Day
    }

    # Use mean of other features for future prediction
    for col in features:
     if col not in input_data:
        input_data[col] = float(df[col].mean())  # Fill missing features silently with mean

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Predict
    prediction = model.predict(input_df[features])
    st.success(f"📈 Predicted Temperature on {Year}-{Month:02d}-{Day:02d}: **{prediction[0]:.2f}°C**")
