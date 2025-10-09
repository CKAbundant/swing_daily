"""Classes to determine slope for a given variable.

- MASLope - Abstract class for testing different sloping method
- PeriodSlope - Concrete class to determine slope based on fixed time period
- AverageSlope - Concrete class to average slope for week, month, 3 months and 6 months
- WeightedSlope - Concrete class to weighted average slope for different time period
- DailySlope - Concrete class to average the daily percentage change for time period
"""

from abc import ABC, abstractmethod

import pandas as pd

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

    @abstractmethod
    def check_slope(self, df: pd.DataFrame, col: str) -> SlopeStatus:
        """Return either 1 (slope up), 0 (sideway), or -1 (slope down)
        given OHLC DataFrame.

        Args:
            df (pd.DataFrame):
                DataFrame containing variable to test slope.
            col (str):
                Name of column in DataFrame that contains the required variable.

        Returns:
            SlopeStatus:
                Whether moving average is sloping up, down or sideway.
        """

    ...
