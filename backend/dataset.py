import pandas as pd
import os

def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, "data", "titanic.csv")
    df = pd.read_csv(file_path)
    return df