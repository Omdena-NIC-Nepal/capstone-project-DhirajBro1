import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess_climate_data(path_to_csv):
    df = pd.read_csv(path_to_csv)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Flag extremely hot days (>35°C) and dry days (<1 mm)
    df['hot_day'] = df['MaxTemp_2m'] > 35
    df['dry_day'] = df['Precip'] < 1

    # Group by District
    grouped = df.groupby('District').agg({
        'Precip': 'mean',
        'Temp_2m': 'std',
        'hot_day': 'sum',
        'dry_day': 'sum'
    }).reset_index()

    grouped.columns = ['District', 'avg_precip', 'temp_std', 'hot_days', 'dry_days']

    # Normalize values between 0 and 1
    scaler = MinMaxScaler()
    features = ['avg_precip', 'temp_std', 'hot_days', 'dry_days']
    grouped[features] = scaler.fit_transform(grouped[features])

    # Calculate vulnerability index (adjust weights as needed)
    grouped['vulnerability_index'] = (
        0.3 * grouped['temp_std'] +
        0.3 * grouped['hot_days'] +
        0.2 * grouped['dry_days'] + 
        0.2 * (1 - grouped['avg_precip'])  # Inverse because low precip → more vulnerable
    )

    return grouped
