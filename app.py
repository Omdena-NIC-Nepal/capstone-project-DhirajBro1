import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Nepal Climate Change Dashboard", page_icon="🌏", layout="wide")

# Main Page
st.title("🌏 Nepal Climate Change Dashboard")
st.markdown("""
Welcome to the Nepal Climate Change Impact Dashboard!  
Here you can explore various analyses on:
- Extreme Weather Events
    - Visualize the frequency and impact of extreme weather events in Nepal.
- Temperature and Rainfall Trends
    - Interactive graphs of long-term temperature data and anomalies.
- NLP Analysis
    - See insights from news/articles/social media using Natural Language Processing.
- Model Training 
    - Train and evaluate machine learning models to predict climate-related outcomes.
- Climate Vulnerability 
    - Explore district-level climate vulnerability based on various environmental and socio-economic indicators.

👉 Use the sidebar to navigate different pages!
""")

col1, col2, col3 = st.columns(3)

col1.metric("Avg Temp Rise", "1.3°C", "+0.5°C")
col2.metric("Floods Reported", "27", "↑ 15%")
col3.metric("CO₂ ppm", "421", "+2.1 ppm")

st.subheader("📉 Sample Trend")
import pandas as pd
import numpy as np

years = np.arange(2000, 2023)
temps = np.random.normal(22, 1.2, size=len(years))
df = pd.DataFrame({"Year": years, "Avg Temperature": temps})
st.line_chart(df.set_index("Year"))

