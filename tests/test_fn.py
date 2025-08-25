import pandas as pd


def test_fn():
    df = pd.read_parquet("./data/AAPL.parquet")

    print(f"\n\n{df}\n")
