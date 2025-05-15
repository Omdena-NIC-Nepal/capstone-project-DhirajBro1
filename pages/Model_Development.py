# model_prediction.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from utils.data_loader import load_temperature_data
from utils.ML_model_dev import (
    multiple_linear_regression,
    ridge_regression,
    lasso_regression,
    gradient_boosting_regression,
    cross_validate_model
)


# Streamlit UI
st.title("🌡️ Train & Predict Temperature Models with Performance Evaluation")

# Load and preprocess data
df = load_temperature_data()
df = df.select_dtypes(include=[np.number]).dropna()

target = 'Temp_2m'
if target not in df.columns:
    st.error(f"❌ Dataset must have a '{target}' column.")
    st.stop()

features = [col for col in df.columns if col != target]
X = df[features]
y = df[target]

# Sidebar model selection
st.header("📌 Select Regression Model")
model_choice = st.selectbox("", [
    "Multiple Linear Regression",
    "Ridge Regression",
    "Lasso Regression",
    "Gradient Boosting Regression"
])

# Sidebar cross-validation option
run_cv = st.checkbox("Run cross-validation (5-fold)", value=False)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = None
y_pred = None

if st.button("🚀 Train and predict model"):
    with st.spinner("Training model..."):
        if model_choice == "Multiple Linear Regression":
            model = multiple_linear_regression(X_train, y_train)
        elif model_choice == "Ridge Regression":
            model = ridge_regression(X_train, y_train)
        elif model_choice == "Lasso Regression":
            model = lasso_regression(X_train, y_train)
        elif model_choice == "Gradient Boosting Regression":
            model = gradient_boosting_regression(X_train, y_train)
    
    # Make predictions on test set
    y_pred = model.predict(X_test)

    # Show evaluation metrics
    rmse = np.sqrt(np.mean((y_test - y_pred)**2))
    mae = np.mean(np.abs(y_test - y_pred))
    r2 = model.score(X_test, y_test)

    st.success("✅ Model trained successfully!")
    st.subheader("📊 Model Performance on Test Set")
    st.write(f"**RMSE:** {rmse:.2f}")
    st.write(f"**MAE:** {mae:.2f}")
    st.write(f"**R² Score:** {r2:.2f}")

    # Optional cross-validation
    if run_cv:
        st.subheader("🔄 Cross-Validation Scores (5-fold)")
        with st.spinner("Running cross-validation..."):
            cross_validate_model(model, X, y, cv=5)

# Prediction section
st.header("📅 Predict Temperature")

Year = st.slider("Year", 2025, 2050, 2025)
Month = st.slider("Month", 1, 12, 1)
Day = st.slider("Day", 1, 31, 1)

if model:
    input_data = {'Year': Year, 'Month': Month, 'Day': Day}
    for col in features:
        if col not in input_data:
            input_data[col] = float(df[col].mean())

    input_df = pd.DataFrame([input_data])

    try:
        prediction = model.predict(input_df[features])
        st.success(f"📈 Predicted Temperature on {Year}-{Month:02d}-{Day:02d}: **{prediction[0]:.2f}°C**")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
