import pandas as pd

def load_csv_to_dataframe(csv_file):
    df = pd.read_csv(csv_file)
    return df
