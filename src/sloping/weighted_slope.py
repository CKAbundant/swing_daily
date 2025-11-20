"""Concrete implementation of 'DetSlope' to determine slope by weighted-averaging
slope for week, month, 3 months and 6 months."""

from datetime import datetime

import numpy as np
import pandas as pd

from src.sloping.base import DetSlope
from src.utils.constants import PeriodUnit, SlopeStatus
from src.utils.utils import cal_percent_change


class WeightedSlope(DetSlope):
    """Determine slope by weighted-averaging slope for a week, a month,
    3 months and 6 months.

    Usage:
        >>> params = [
            ("week", 1, 0.4),
            ("month", 1, 0.3),
            ("month", 3, 0.2),
            ("month", 6, 0.1),
        ]
        >>> weighted_slope = AverageSlope(threshold=0.05, params)
        >>> slope = weighted_slope.det_slope(df, "sma_20")

    Args:
        params (list[tuple[str, int, float]]):
            List containing period_unit (i.e. day, week, month), period and weights.

    Attributes:
        params (list[tuple[str, int, float]]):
            List containing period_unit (i.e. day, week, month), period and weights.

    """

    def __init__(self, params: list[tuple[str, int, float]], threshold: float = 0.05):
        super().__init__(threshold)
        self.params = params

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

        weighted_av = 0

        for period_unit, period, weights in self.params:
            percent_change = cal_percent_change(
                df, var, latest_date, period_unit, period
            )
            weighted_av += percent_change * weights

        return self._compute_slope(weighted_av)
