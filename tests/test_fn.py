import finnhub
import numpy as np
import pandas as pd
import talib


def test_fn():
    df = pd.read_parquet("./data/AAPL.parquet")
    API_KEY = "d2mkd99r01qog44448v0d2mkd99r01qog44448vg"

    print(f"\n\n{df}\n")

    for col in df.columns:
        data_type = {type(record) for record in df[col]}
        print(f"{col} : {data_type}")

    atr = getattr(talib, "ATR")(df["High"], df["Low"], df["Close"])
    print(f"\n\n{atr=}\n")

    atr_type = {type(record) for record in atr}
    print(f"{atr_type=}")
