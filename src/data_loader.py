import pandas as pd


def load_invoices(file_path="data/invoices.csv"):
    """
    Load invoice data from a CSV file and return a Pandas DataFrame.
    """
    df = pd.read_csv(file_path)
    return df