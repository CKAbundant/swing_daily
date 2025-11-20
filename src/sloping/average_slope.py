"""Concrete implementation of 'DetSlope' to determine slope by averaging slope
for week, month, 3 months and 6 months."""

from src.sloping.base import DetSlope


class AverageSlope(DetSlope):
    """Determine slope by averaging slope for a week, a month, 3 months and 6 months.

    Usage:
        >>> average_slope = AverageSlope(threshold=0.05)
        >>> slope = average_slope.det_slope(df, "sma_20")
    """
