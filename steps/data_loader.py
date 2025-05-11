import pandas as pd
from zenml import step

@step
def load_data() -> (pd.DataFrame):
    df = pd.read_csv("data/training.csv", index_col=0)
    return df
