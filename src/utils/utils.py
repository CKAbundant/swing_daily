"""Helper functions for implementing Swing Daily trading strategy."""

import calendar
from datetime import datetime, timedelta
from decimal import Decimal

import pandas as pd

from src.utils.constants import PeriodUnit


def cal_percent_change(
    df: pd.DataFrame, var: str, end_date: datetime, period_unit: PeriodUnit, period: int
) -> Decimal:
    """Compute percentage change for required variable given start and latest date.

    Args:
        df (pd.DataFrame): DataFrame containing variable to test slope.
        var (str): Variable used to determine slope.
        start_date (datetime): Start date to compute slope.
        period_unit (PeriodUnit): Either days, weeks or months.
        period (int): Number of 'period_unit' to compute slope.

    Returns:
        percent_change (Decimal):
            Percentage change of required variable given start and end date.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("'df' is not a DataFrame.")

    if var not in df.columns:
        raise ValueError(f"{var} is not a column in 'df' DataFrame.")

    # Get start date
    start_date = _get_start_date(end_date, period_unit, period)

    # Get start, end level and percent change to determine slope
    start_level = _get_level(df, start_date, var)
    end_level = _get_level(df, end_date, var)
    percent_change = (end_level - start_level) / start_level

    print(f"\n\nlatest_date : {end_date} -> {end_level}")
    print(f"start_date : {start_date} -> {start_level}\n")
    print(f"percent_change : {percent_change}")

    return percent_change


def _get_start_date(
    end_date: datetime, period_unit: PeriodUnit, period: int
) -> datetime:
    """Get start date based on latest record in DataFrame."""
    if period_unit == "month":
        return _get_start_date_by_month(end_date, period)

    if period_unit == "week":
        days = period * 7
        return end_date - timedelta(days=days)

    if period_unit == "day":
        return end_date - timedelta(days=period)


def _get_start_date_by_month(end_date: datetime, period: int) -> datetime:
    """Get start date if period is based on number of months."""

    current_month = end_date.month
    current_year = end_date.year
    start_date = end_date.day

    # Convert periods in months to year and month
    period_year = period // 12
    period_month = period % 12

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
    start_date = start_date if end_date.day <= last_day else last_day

    # Start day remains the same since period is based on month
    return datetime(start_year, start_month, start_date)


def _get_level(df: pd.DataFrame, dt: datetime, var: str) -> Decimal:
    """Get value of required variable at specific date to determine slope.

    Args:
        df (pd.DataFrame): DataFrame containing info of required variable.
        dt (datetime): Date used to determine value of required variable.
        var (str): Variable used to determine slope.

    Returns:
        (Decimal): Value of required variable.
    """

    if "date" not in df.columns:
        raise ValueError("'date' column is not present in DataFrame.")

    # Keep going back 1 day until trading day is available
    while dt not in df["date"].to_list():
        dt = dt - timedelta(days=1)

    return df.loc[df["date"] == dt, var].item()
