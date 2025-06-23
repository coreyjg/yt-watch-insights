from pathlib import Path

def save_to_parquet(df, output_path='output/watch_history.parquet'):
    """
    Save the cleaned DataFrame to a Parquet file for efficient I/O and querying.

    Args:
        df (pd.DataFrame): Cleaned watch history data.
        output_path (str): Where to write the .parquet file.
    """
    # Ensure the output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    # Write to Parquet without the index column
    df.to_parquet(output_path, index=False)
