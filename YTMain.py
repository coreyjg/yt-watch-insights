from YTExtract import extract_watch_history
from YTTransform import clean_data
from YTLoad import save_to_parquet
import pandas as pd

# Extract raw data from JSON
df = extract_watch_history('watch-history.json')

# Clean and enrich the raw DataFrame
df_clean = clean_data(df)

# Persist cleaned data to Parquet for dashboard consumption
save_to_parquet(df_clean)

# Configure pandas display options for debugging
pd.set_option('display.max_columns', None)

