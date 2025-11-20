"""Concrete implementation of 'DetSlope' to determine slope by averaging slope
for week, month, 3 months and 6 months."""

from datetime import datetime

import numpy as np
import pandas as pd

from src.sloping.base import DetSlope
from src.utils.constants import PeriodUnit, SlopeStatus
from src.utils.utils import cal_percent_change


class AverageSlope(DetSlope):
    """Determine slope by averaging slope for a week, a month, 3 months and 6 months.

    Usage:
        >>> average_slope = AverageSlope(threshold=0.05)
        >>> slope = average_slope.det_slope(df, "sma_20")
    """

    def det_slope(self, df: pd.DataFrame, var: str) -> SlopeStatus:
        """Return either 1 (slope up), 0 (sideway), or -1 (slope down) for var
        given OHLC DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing variable to test slope.
            var (str): Variable used to determine slope.

        Returns:
            SlopeStatus: Whether moving average is sloping up, down or sideway.
        """

        df = self._format_df(df, var)

        # Get latest date
        latest_date = df["date"].max()

        # Get percent change for 1 week, 1 month, 3 months and 6 months
        info = [
            ("week", 1),
            ("month", 1),
            ("month", 3),
            ("month", 6),
        ]

        # Compute average percentage change
        av_percent_change = np.mean(
            [
                cal_percent_change(df, var, latest_date, period_unit, period)
                for period_unit, period in info
            ]
        )

        return self._compute_slope(av_percent_change)
