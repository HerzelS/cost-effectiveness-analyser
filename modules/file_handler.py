import pandas as pd

def load_file(uploaded_file):
    """
    Load a file into a pandas DataFrame.

    Args:
        uploaded_file: The file to be loaded, which can be a CSV, Excel, or JSON file.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV, Excel file.")
    return df