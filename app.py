import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

# Set page config
st.set_page_config(page_title="Nepal Climate Change Dashboard", page_icon="🌏", layout="wide")

# Main Page
st.title("🌏 Nepal Climate Change Dashboard")
st.markdown("""
Welcome to the Nepal Climate Change Impact Dashboard!  
Here you can explore various analyses on:
- Extreme Weather Events
- Temperature and Rainfall Trends
- Glacial Lake Monitoring
- Flood Risk Mapping
- Population Vulnerability

👉 Use the sidebar to navigate different pages!
""")

