import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

# ====================================
# 1. Climate Indices Engineering
# ====================================
def create_climate_indices(weather_df):
    weather_df['drought_index'] = weather_df['prectot'] / weather_df['t2m']  # Simple drought index
    weather_df['heat_stress_index'] = weather_df['t2m_max'] - weather_df['rh2m']  # Heat stress
    return weather_df
# ====================================
# 2. Seasonal Monsoon Indicators
# ====================================
def create_monsoon_indicators(weather_df):
    weather_df['is_monsoon'] = weather_df['month'].apply(lambda x: 1 if x in [6,7,8,9] else 0)  # June to September
    return weather_df

# ====================================
# 3. Lag Features for Time-Series
# ====================================
def create_lag_features(df, column_list, lags=[1,2,3]):
    for col in column_list:
        for lag in lags:
            df[f'{col}_lag{lag}'] = df[col].shift(lag)
    return df

# ====================================
# 4. Spatial Proximity Features
# ====================================
def create_spatial_features(df, lat_col='lat', lon_col='lon', n_neighbors=5):
    coords = df[[lat_col, lon_col]].dropna()
    neighbors = NearestNeighbors(n_neighbors=n_neighbors)
    neighbors.fit(coords)
    distances, indices = neighbors.kneighbors(coords)
    df['avg_neighbor_distance'] = distances.mean(axis=1)
    return df

# ====================================
# 5. Extract Features from Satellite Imagery
# ====================================
def extract_satellite_features(lulc_df):
    # Example: Calculate land cover type counts
    lulc_counts = lulc_df['LULC_Label'].value_counts().to_dict()
    lulc_features = pd.DataFrame([lulc_counts])
    return lulc_features

# ====================================
# 6. Integrate Geographic Information
# ====================================
def integrate_geographic_info(df, elevation_df):
    merged_df = df.merge(elevation_df, on='district', how='left')
    return merged_df

# ====================================
# 7. Normalize and Scale Features
# ====================================
def normalize_features(df, columns_to_scale):
    scaler = StandardScaler()
   
    df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
    return df

# ====================================
# 8. Dimensionality Reduction (Optional)
# ====================================
def perform_dimensionality_reduction(df, n_components=5):
    pca = PCA(n_components=n_components)
    reduced_features = pca.fit_transform(df.dropna(axis=1))
    reduced_df = pd.DataFrame(reduced_features, columns=[f'PC{i+1}' for i in range(n_components)])
    return reduced_df