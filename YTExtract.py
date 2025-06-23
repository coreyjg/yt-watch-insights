import json
import pandas as pd

def extract_watch_history(json_path):
    """
    Read YouTube watch history JSON and convert to a flat DataFrame.

    Args:
        json_path (str): Path to the JSON file containing watch history entries.

    Returns:
        pd.DataFrame: DataFrame with columns title, url, channel, time.
    """
    # Open the JSON file with UTF-8 and replace errors to avoid decode issues
    with open(json_path, 'r', encoding='utf-8', errors='replace') as f:
        data = json.load(f)

    records = []
    # Iterate over each history entry in the JSON array
    for entry in data:
        # Only include entries that have a 'titleUrl' (actual watch events)
        if 'titleUrl' in entry:
            records.append({
                'title': entry.get('title'),              # Video or playlist title
                'url': entry.get('titleUrl'),              # Link to the video/watch event
                'channel': entry.get('subtitles', [{}])[0].get('name'),  # First subtitle name = channel
                'time': entry.get('time')                  # Timestamp string from JSON
            })
    # Convert the list of dicts to a DataFrame for downstream processing
    return pd.DataFrame(records)
