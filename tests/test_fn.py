import calendar
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import talib

from src.sloping.period_slope import PeriodSlope
from src.utils.utils import cal_percent_change
from tests.utils.test_utils import list_datatype


def test_fn(sample_df):
    info = [
        ("week", 1),
        ("month", 1),
        ("month", 3),
        ("month", 6),
    ]

    df = sample_df.copy()
    df.columns = [col.lower() for col in df.columns]

    a = np.mean(
        [cal_percent_change(df, "close", datetime(2025, 5, 15), a, b) for a, b in info]
    )

    print(f"\n{a}\n")
