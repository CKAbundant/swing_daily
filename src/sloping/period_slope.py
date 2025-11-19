"""Concrete implementation of 'DetSlope' to determine slope based on
fixed time period i.e. by days, weeks or months."""

import calendar
from datetime import datetime, timedelta

import pandas as pd

from src.sloping.base import DetSlope
from src.utils.constants import PeriodUnit, SlopeStatus


class PeriodSlope(DetSlope):
    """Determine slope based on fixed time period.

    Usage:
        >>> period_slope = PeriodSlope("month", 6)
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

    def det_slope(self, df: pd.DataFrame, col_name: str) -> SlopeStatus:
        """Return either 1 (slope up), 0 (sideway), or -1 (slope down)
        given OHLC DataFrame.

        Args:
            df (pd.DataFrame):
                DataFrame containing variable to test slope.
            col_name (str):
                Name of column in DataFrame that contains the required variable.

        Returns:
            SlopeStatus:
                Whether moving average is sloping up, down or sideway.
        """

        df = self._validate_df(df)

        # Get latest date
        latest_date = df["date"].max()

        # Get start date
        start_date = self._get_start_date(latest_date)

    def _validate_period(self) -> None:
        """Validate period must be positive."""

        if self.period <= 0:
            raise ValueError("Period must be positive!")

        if not isinstance(self.period, int):
            raise ValueError("period must be an integer!")

        if self.period_unit not in ["day", "week", "month"]:
            raise ValueError("period unit must be 'day', 'week' or 'month'!")

    def _get_start_date(self, latest_date: datetime) -> datetime:
        """Get start date based on latest record in DataFrame."""
        if self.period_unit == "month":
            return self._get_start_date_by_month(latest_date)

        if self.period_unit == "week":
            days = self.period * 7
            return latest_date - timedelta(days=days)

        if self.period_unit == "day":
            return latest_date - timedelta(days=self.period)

    def _get_start_date_by_month(self, latest_date: datetime) -> datetime:
        """Get start date if period is based on number of months."""

        current_month = latest_date.month
        current_year = latest_date.year
        start_date = latest_date.day

        # Convert periods in months to year and month
        period_year = self.period // 12
        period_month = self.period % 12

        # Compute difference between current_month and period_month
        # and current_year and period_year
        diff_month = current_month - period_month
        diff_year = current_year - period_year

        # if diff_month is negative, increment period_year by 1 and
        # diff_month by 12
        start_month = diff_month if diff_month > 0 else diff_month + 12
        start_year = diff_year if diff_month > 0 else diff_year - 1

        # Set start date to last day for start_month and start_year if out of range
        _, last_day = calendar.monthrange(start_year, start_month)
        start_date = start_date if latest_date.day <= last_day else last_day

        # Start day remains the same since period is based on month
        return datetime(start_year, start_month, start_date)
