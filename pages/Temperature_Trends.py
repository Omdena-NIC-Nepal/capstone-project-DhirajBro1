import streamlit as st
#from utils.data_loader import load_weather_events,load_temperature_data
import utils.data_loader as dl
#from utils.plots import plot_temperature_trends, plot_precipitation_trends, plot_monthly_avg
import utils.plots as p

# Set page config
st.set_page_config(page_title="Temperature & Rainfall Trends", layout="wide")

# Title
st.title(" Temperature & Rainfall Trends in Nepal")

# Load data
df = dl.load_temperature_data()

# Sidebar Filters
st.sidebar.header("Filter Options")

districts = df['District'].dropna().unique().tolist()
selected_districts = st.sidebar.multiselect("Select District(s):", districts, default=districts[:3])

years = sorted(df['Year'].dropna().unique())
selected_years = st.sidebar.slider("Select Year Range:", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))

# Filter data
filtered_df = df[
    (df['District'].isin(selected_districts)) &
    (df['Year'] >= selected_years[0]) &
    (df['Year'] <= selected_years[1])
]

# Plotting
st.subheader(" Average Temperature Over Time")
fig1 = p.plot_temperature_trends(filtered_df, selected_districts)
st.pyplot(fig1)

st.subheader(" Precipitation Over Time")
fig2 = p.plot_precipitation_trends(filtered_df, selected_districts)
st.pyplot(fig2)