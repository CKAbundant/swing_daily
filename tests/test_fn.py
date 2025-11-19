import calendar
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import talib

from src.sloping.period_slope import PeriodSlope
from tests.utils.test_utils import list_datatype


def test_fn():
    latest_date = datetime(2025, 12, 31)
    threshold = 0.05
    period_unit = "month"
    period = 58

    period_slope = PeriodSlope(threshold, period_unit, period)
    start_date = period_slope._get_start_date_by_month(latest_date)

    print(f"\n\nlatest_date : {latest_date}")
    print(f"period : {period}")
    print(f"start_date : {start_date}\n")
