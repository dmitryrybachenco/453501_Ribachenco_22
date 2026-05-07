import pandas as pd

def load_salary_data_from_file(filepath: str) -> pd.DataFrame:
    """
    Load Salary dataset from a specific CSV file

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame with Salary data
    """
    try:
        df = pd.read_csv(filepath)
        print(f"   Loaded data from {filepath}")
        return df
    except FileNotFoundError:
        print(f" File not found: {filepath}")
        raise
    except Exception as e:
        print(f" Error loading file: {e}")
        raise