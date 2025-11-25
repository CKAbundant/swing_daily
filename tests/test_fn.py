import calendar
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import talib

from src.sloping.daily_slope import DailySlope
from src.utils.utils import cal_percent_change
from tests.utils.test_utils import list_datatype


def test_fn(sample_df):
    print(f"\n\n{sample_df}\n")

    a = sample_df.loc[
        (sample_df["Date"] >= datetime(2025, 4, 12))
        & (sample_df["Date"] <= datetime(2025, 6, 1)),
        :,
    ]
    print(f"\n\n{a}\n")

    b = a["Close"].pct_change()
    b = b.dropna()

    print(f"\n{b}\n")
    print(f"\n{b.to_numpy()}\n")
    print(f"{b.to_numpy().mean()}\n")
