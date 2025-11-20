import calendar
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import talib

from src.sloping.period_slope import PeriodSlope
from tests.utils.test_utils import list_datatype


def test_fn(sample_df):
    print(f"\n\n{sample_df}\n")
