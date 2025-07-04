import pandas as pd
import streamlit as st

# Load the cleaned watch history data
# Data is expected in Parquet format for efficient I/O
# Ensure you ran extract/transform/load steps before this

df = pd.read_parquet('output/watch_history.parquet')

# Title for the Streamlit app
st.title("MY YOUTUBE WATCH HISTORY")

# -----------------------------
# Sidebar filters
# -----------------------------
# Let the user pick a start and end date for filtering the data.
# Defaults to the full range of available dates in the dataset.
start, end = st.sidebar.date_input(
    "Date Range",
    [df['time'].dt.date.min(), df['time'].dt.date.max()]
)

# Apply date filter first to include all channels for the charts
df_date_filtered = df[
    df['time'].dt.date.between(start, end)
]

# Count views per channel (sorted descending by default)
channel_counts    = df_date_filtered['channel'].value_counts()
# Get a list of channels, most-viewed first
ordered_channels  = channel_counts.index.tolist()

# Allow the user to select one or more channels to include.
# Defaults to all channels present in the DataFrame.
selected = st.sidebar.multiselect(
    "Channels",
    options=ordered_channels,
    default=ordered_channels
)

# Filter the date‐filtered DataFrame by the user’s channel selection
df_for_charts = df_date_filtered[
    df_date_filtered['channel'].isin(selected)
].copy()

# -----------------------------
# Hourly Chart
# -----------------------------
# Group by hour_label (e.g., "0:00", "13:00") to count views per hour
hourly_counts = df_for_charts.groupby('hour_label').size()

# Create labels for all 24 hours to ensure consistent ordering
labels = [f"{h}:00" for h in range(24)]
# Reindex to fill any missing hours with zero views
hourly_counts = hourly_counts.reindex(labels, fill_value=0)

# Convert index to an ordered categorical for proper x-axis ordering
hourly_counts.index = pd.CategoricalIndex(
    hourly_counts.index,
    categories=labels,
    ordered=True
)

# Section heading and subheading for the hourly chart
st.header("What Time Of Day Do I Watch The Most YouTube")
st.subheader("Views by Hour of the Day")
# Render bar chart for hourly counts
st.bar_chart(hourly_counts)

# -----------------------------
# Daily Chart
# -----------------------------
# Group by day name (e.g., Monday, Tuesday) to count views per weekday
daily_counts = (
    df_for_charts.groupby("day")
      .size()               # count rows per day
      .reindex([
          'Monday','Tuesday','Wednesday','Thursday',
          'Friday','Saturday','Sunday'
      ], fill_value=0)       # ensure all days appear
      .reset_index(name='count')  # convert to DataFrame for plotting
)

# Section heading and subheading for the daily chart
st.header("What Day Of The Week Do I Watch The Most YouTube")
st.subheader("Views by Day of the Week")
# Render bar chart for daily counts
st.bar_chart(daily_counts.set_index('day')['count'])

# -----------------------------
# Month-over-Month Views
# -----------------------------
# Use the timestamp as the index for time-based resampling
# Resample at month-end frequency and count number of entries per period
mom_count = (
    df_for_charts.set_index('time')
      .resample('ME')      # use 'ME' (month end) to avoid deprecation warning
      .size()              # count entries in each monthly bucket
      .rename('views')     # name the resulting Series
)

# Section heading and subheading for MoM line chart
st.header("How Has My Viewing Changed Over Time")
st.subheader("Month Over Month Views")
# Render line chart of monthly view counts
st.line_chart(mom_count)
