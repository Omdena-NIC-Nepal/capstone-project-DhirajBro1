import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd

def line_plot(x, y, xlabel="", ylabel="", title=""):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(x, y, marker='o')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    return fig

def bar_plot(x, y, xlabel="", ylabel="", title=""):
    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return fig

def heatmap_corr(df, title="Correlation Heatmap"):
    fig, ax = plt.subplots(figsize=(10,8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title(title)
    return fig


def plot_events_over_time(df):
    fig, ax = plt.subplots(figsize=(12,6))
    events_over_time = df['start_date'].value_counts().sort_index()
    ax.plot(events_over_time.index, events_over_time.values, marker='o')
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Events")
    ax.grid(True)
    return fig

def plot_disaster_type_distribution(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.countplot(y='Disaster Type', data=df, order=df['Disaster Type'].value_counts().index, ax=ax)
    return fig

def plot_correlation_heatmap(df):
    fig, ax = plt.subplots(figsize=(10,8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
    return fig

def plot_temperature_trends(df, selected_DNMs):
    fig, ax = plt.subplots(figsize=(12,6))
    sns.lineplot(data=df[df['District'].isin(selected_DNMs)], x="Year", y="Temp_2m", hue="District", ax=ax, marker="o")
    ax.set_ylabel("Avg Temperature (°C)")
    ax.set_xlabel("Year")
    ax.grid(True)
    return fig

def plot_precipitation_trends(df, selected_DNMs):
    fig, ax = plt.subplots(figsize=(12,6))
    sns.lineplot(data=df[df['District'].isin(selected_DNMs)], x="Year", y="Precip", hue="District", ax=ax, marker="o")
    ax.set_ylabel("Precipitation (mm)")
    ax.set_xlabel("Year")
    ax.grid(True)
    return fig

def plot_monthly_avg(df):
    monthly_df = df.groupby('month')[['Temp_2m', 'Precip']].mean().reset_index()
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    sns.barplot(data=monthly_df, x='month', y='Temp_2m', ax=axes[0], palette="coolwarm")
    axes[0].set_title("Monthly Avg Temperature (°C)")
    axes[0].grid(True)

    sns.barplot(data=monthly_df, x='month', y='Precip', ax=axes[1], palette="Blues")
    axes[1].set_title("Monthly Avg Rainfall (mm)")
    axes[1].grid(True)

    return fig
import plotly.express as px
def plot_climate_vulnerability_map(df):
    gdf_flood=gpd.read_file('data/processed_data/flood_data.geojson')
    gdf_flood['vulnerability_index'] = gdf_flood['FLOOD_FREQ'] / gdf_flood['FLOOD_FREQ'].max()
    fig = px.choropleth(
        gdf_flood,
        geojson=gdf_flood,
        locations='District',
        featureidkey='properties.District',
        color='vulnerability_index',
        color_continuous_scale='YlOrRd',
        labels={'vulnerability_index': 'Vulnerability Index'},
        title='Climate Vulnerability Map of Nepal'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
    return fig



def plot_climate_vulnerability_map(gdf, column='vulnerability_index', title='Climate Vulnerability'):
    # Create folium map
    m = folium.Map(location=[28.5, 84], zoom_start=7, tiles='CartoDB positron')

    # Add choropleth
    folium.Choropleth(
        geo_data=gdf,
        name="choropleth",
        data=gdf,
        columns=["District", column],
        key_on="feature.properties.District",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=title
    ).add_to(m)

    # Add hover labels
    for _, r in gdf.iterrows():
        folium.Popup(f"{r['District']}: {r[column]:.2f}").add_to(
            folium.Marker(location=[r.geometry.centroid.y, r.geometry.centroid.x])
        )

    st_folium(m, width=1000, height=600)
