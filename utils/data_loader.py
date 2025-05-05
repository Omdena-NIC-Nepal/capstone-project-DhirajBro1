# import pandas as pd
# import streamlit as st
# import geopandas as gpd

# @st.cache_data
# def load_weather_events():
#     return pd.read_csv('data/processed_data/processed_extreme_weather_events.csv')

# @st.cache_data
# def load_temperature_data():
#     return pd.read_csv('data/processed_data/dailyclimate.csv')

# @st.cache_data
# def load_glacial_data():
#     return pd.read_csv('data/processed_data/processed_glacial_lake_data.csv')

# @st.cache_data
# def load_flood_data():
#     return pd.read_csv('data/processed_data/flood_data.csv')

# @st.cache_data
# def load_population_data():
#     return pd.read_csv('data/processed_data/processed_population_data.csv')

# @st.cache_data
# def load_flood_geojson():
#     return gpd.read_file('data/processed_data/flood_data.geojson')



import pandas as pd
import streamlit as st
import geopandas as gpd

@st.cache_data
def load_weather_events():
    return pd.read_csv('data/processed_data/processed_extreme_weather_events.csv')

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

def main():
    st.title("Climate Change Data Explorer - Nepal")
    
    data_options = {
        "Extreme Weather Events": load_weather_events,
        "Temperature Data": load_temperature_data,
        "Glacial Lake Data": load_glacial_data,
        "Flood Data": load_flood_data,
        "Population Data": load_population_data,
        "Flood GeoJSON (Map)": load_flood_geojson
    }

    choice = st.sidebar.selectbox("Select Dataset", list(data_options.keys()))
    df = data_options[choice]()

    st.write(f"### Showing {choice}")
    st.dataframe(df.head())

if __name__ == "__main__":
    main()
