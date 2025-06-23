import pandas as pd

def clean_data(df):
    """
    Clean and enrich the raw watch history DataFrame.

    Adds datetime parsing, fills missing data, and extracts time features.
    """
    # Parse the 'time' strings into pandas Timestamps (UTC-aware)
    df['time'] = pd.to_datetime(df['time'], errors='coerce', utc=True)

    # Fill any missing channel names with a placeholder
    df['channel'] = df['channel'].fillna('Unknown')

    # Extract numeric hour (0–23) from the timestamp
    df['hour'] = df['time'].dt.hour

    # Extract weekday name, e.g., 'Monday'
    df['day'] = df['time'].dt.day_name()

    # Extract calendar year of the watch event
    df['year'] = df['time'].dt.year

    # Extract numeric month (1–12)
    df['month'] = df['time'].dt.month

    # Remove rows where hour parsing failed (NaN)
    df = df.loc[df['hour'].notna()].copy()

    # Create a human-readable label for the hour bucket, e.g., '13:00'
    df['hour_label'] = df['hour'].apply(lambda h: f"{int(h)}:00")

    return df
