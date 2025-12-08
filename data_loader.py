from datasets import load_dataset
import pandas as pd
import os

def load_data(split='workforce'):
    """
    Loads the Anthropic Interviewer dataset.
    
    Args:
        split (str): The dataset split to load (e.g., 'workforce', 'creatives', 'scientists').
        
    Returns:
        pd.DataFrame: The loaded data as a Pandas DataFrame.
    """
    print(f"Loading dataset split: {split}...")
    try:
        dataset = load_dataset("Anthropic/AnthropicInterviewer", split=split)
        df = dataset.to_pandas()
        print(f"Successfully loaded {len(df)} rows.")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

if __name__ == "__main__":
    # Test loading
    df = load_data()
    if df is not None:
        print(df.head())
        print(df.columns)
