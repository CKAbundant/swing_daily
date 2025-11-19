"""Abstract Class to determine slope for a given variable.

- DetSLope - Abstract class for testing different sloping method
- PeriodSlope - Concrete class to determine slope based on fixed time period
- AverageSlope - Concrete class to average slope for week, month, 3 months and 6 months
- WeightedSlope - Concrete class to weighted average slope for different time period
- DailySlope - Concrete class to average the daily percentage change for time period
"""

from abc import ABC, abstractmethod

import pandas as pd
from strat_backtest.utils import set_datetime, set_decimal_type

from src.utils.constants import SlopeStatus


class DetSlope(ABC):
    """Abstract class for different sloping method.

    Args:
        threshold (float):
            Minimum percentage change to qualify for slope (Default: 0.01).

    Attributes:
        threshold (float):
            Minimum percentage change to qualify for slope (Default: 0.01).
    """

    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold

    @abstractmethod
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

    ...

    def _format_df(self, df: pd.DataFrame, var: str) -> pd.DataFrame:
        """Ensure DataFrame has the required column and date field.

        Args:
            df (pd.DataFrame):
                DataFrame containing variable to test slope.
            var (str):
                Variable used to determine slope.

        Returns:
            df (pd.DataFrame): Formatted and validated DataFrame.
        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' is not a DataFrame type.")

        # Ensure DataFrame doesn't contain null values
        for col in df.columns:
            if df[col].isna().any():
                raise ValueError(f"'{col}' column contain null values.")

        # Lowercase column headings
        df.columns = [col.lower() for col in df.columns]

        # Check if 'date' column exist
        for col in ["date", var]:
            if col not in df.columns:
                raise ValueError(f"'{col}' column doesn't exist!")

        # Reset index if index has name
        if df.index.name is not None:
            df = df.reset_index()

        # Set date-related column to datetime type
        df = set_datetime(df)

        # Set numeric type to be Decimal type
        df = set_decimal_type(df)

        # Sort DataFrame by date
        df = df.sort_values(by=["date"], ascending=True)

        return df
