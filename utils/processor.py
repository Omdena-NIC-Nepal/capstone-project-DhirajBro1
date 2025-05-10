import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import re
from gensim.summarization import summarize
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
def clean_topics(topic_string):
    # Split by Topic
    topics = topic_string.split(';')
    cleaned = []
    for topic in topics:
        topic = topic.strip()
        if topic:
            # Extract "Topic X" and keywords
            match = re.match(r"(Topic \d+): (.+)", topic)
            if match:
                topic_name = match.group(1)
                keywords = match.group(2)
                # Extract only words, drop weights and quotes
                keywords_list = re.findall(r'"(.*?)"', keywords)
                cleaned.append((topic_name, keywords_list))
    return cleaned
def summarize_text(text, ratio=0.1):
    try:
        summary = summarize(text, ratio=ratio)
        if not summary.strip():
            return "⚠️ Summary not available (text too short or too simple)."
        return summary
    except ValueError:
        return "⚠️ Summary not available (text too short or too simple)."
