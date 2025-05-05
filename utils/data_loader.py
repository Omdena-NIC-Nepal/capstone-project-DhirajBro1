import pandas as pd
import streamlit as st
import geopandas as gpd

@st.cache_data
# def load_weather_events():
#     return pd.read_csv('data/processed_data/processed_extreme_weather_events.csv')
def load_temperature_data():
    file_path = Path(__file__).parent.parent / "data" / "processed_data" / "dailyclimate.csv"
    return pd.read_csv(file_path)

@st.cache_data
def load_temperature_data():
    return pd.read_csv('data/processed_data/dailyclimate.csv')

@st.cache_data
def load_glacial_data():
    return pd.read_csv('data/processed_data/processed_glacial_lake_data.csv')

@st.cache_data
def load_flood_data():
    return pd.read_csv('data/processed_data/flood_data.csv')

@st.cache_data
def load_population_data():
    return pd.read_csv('data/processed_data/processed_population_data.csv')

@st.cache_data
def load_flood_geojson():
    return gpd.read_file('data/processed_data/flood_data.geojson')



