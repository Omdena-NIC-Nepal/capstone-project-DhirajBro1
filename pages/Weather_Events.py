import streamlit as st
import utils.data_loader as data_loader
import utils.plots as plots

# Load data
df = data_loader.load_weather_events()

# Sidebar
st.sidebar.header("Filter Options")
start_year = int(df['start_year'].min())
end_year = int(df['start_year'].max())
year_range = st.sidebar.slider('Select Year Range:', start_year, end_year, (start_year, end_year))
disaster_types = df['disaster_type'].dropna().unique().tolist()
selected_disaster = st.sidebar.multiselect('Select disaster_types:', disaster_types, default=disaster_types)

# Filtered data
filtered_df = df[
    (df['start_year'] >= year_range[0]) & 
    (df['start_year'] <= year_range[1]) & 
    (df['disaster_type'].isin(selected_disaster))
]

# Main
st.title(" Extreme Weather Events Analysis")

# Summary Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Events", filtered_df.shape[0])
col2.metric("Total Deaths", int(filtered_df['total_deaths'].sum()))
col3.metric("Total Affected", int(filtered_df['no._affected'].sum()))

st.markdown("---")

# Line Chart
st.subheader(" Events Over Time")
events_over_time = filtered_df['start_year'].value_counts().sort_index()
fig1 = plots.line_plot(events_over_time.index, events_over_time.values, xlabel="Year", ylabel="Events", title="Events Over Time")
st.pyplot(fig1)

# Bar Plot
st.subheader(" Disaster Type Distribution")
fig2 = plots.bar_plot(filtered_df['disaster_type'].value_counts().index, filtered_df['disaster_type'].value_counts().values,
                      xlabel="disaster_type", ylabel="Count", title="disaster_type Distribution")
st.pyplot(fig2)

# Correlation Heatmap
st.subheader(" Correlation Analysis")
fig3 = plots.heatmap_corr(filtered_df)
st.pyplot(fig3)
