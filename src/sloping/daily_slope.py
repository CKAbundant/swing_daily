"""Concrete implementation of 'DetSlope' to determine slope based on
fixed time period i.e. by days, weeks or months."""

from datetime import datetime, timedelta
from decimal import Decimal

import pandas as pd

from src.sloping.base import DetSlope
from src.utils.constants import PeriodUnit, SlopeStatus
from src.utils.utils import cal_percent_change, get_start_date


class DailySlope(DetSlope):
    """Determine slope based on daily returns over fixed time period.

    Usage:
        >>> daily_slope = DailySlope(threshold=0.05, period_unit="month", period=6)
        # Determine slope for simple moving average (period=20)
        >>> slope = period_slope.det_slope(df, "sma_20")

    Args:
        period_unit (PeriodUnit):
            Either "day", "week", or "month" (Default: "month")
        period (int):
            Number of 'period_unit' to compute slope (Default: 6).

    Attributes:
        period_unit (PeriodUnit):
            Either "day", "week", or "month" (Default: "month").
        period (int):
            Number of 'period_unit' to compute slope.
    """

    def __init__(
        self,
        threshold: float = 0.05,
        period_unit: PeriodUnit = "month",
        period: int = 6,
    ):
        super().__init__(threshold)
        self.period_unit = period_unit
        self.period = period
        self._validate_period()

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

        # Get latest date and start date
        latest_date = df["date"].max()
        start_date = get_start_date(latest_date, self.period_unit, self.period)

        # Compute average daily change
        percent_change = self._compute_av_daily_gain(df, var, start_date)

        return self._compute_slope(percent_change)

    def _validate_period(self) -> None:
        """Validate period must be positive."""

        if self.period <= 0:
            raise ValueError("Period must be positive!")

        if not isinstance(self.period, int):
            raise ValueError("period must be an integer!")

        if self.period_unit not in ["day", "week", "month"]:
            raise ValueError("period unit must be 'day', 'week' or 'month'!")

    def _compute_av_daily_gain(
        self, df: pd.DataFrame, var: str, start_date: datetime
    ) -> Decimal:
        """Compute average daily gain from start date to latest date in DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing variable to test slope.
            var (str): Variable used to determine slope.
            start_date (datetime): Start date to compute slope.

        Returns:
            (Decimal): Average of daily gain over given time period.
        """

        # Get subset of DataFrame based on required time period
        subset = df.loc[(df["date"] >= start_date), :].reset_index()

        # Get daily percentage change and drop null values
        percent_series = subset[var].pct_change()
        percent_series = percent_series.dropna()

        # Compute average daily change
        return percent_series.to_numpy().mean()
