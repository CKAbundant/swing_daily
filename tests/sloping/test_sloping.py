"""Test scripts for concrete implementation of 'DetSlope' abstract class."""

from datetime import datetime

import pytest

from src.sloping.period_slope import PeriodSlope
from tests.utils.test_utils import list_datatype


@pytest.mark.parametrize(
    "threshold, period_unit, period, slope_status",
    [
        (0.02, "day", 5, 1),
        (0.05, "day", 5, 0),
        (0.05, "week", 3, 1),
        (0.05, "month", 4, 1),
    ],
)
def test_period_slope(sample_df, threshold, period_unit, period, slope_status):
    # def test_period_slope(sample_df):
    """Test if slope is determined correctly via PeriodSlope"""

    # print(f"\n\n{sample_df.tail(20)}\n")

    period_slope = PeriodSlope(threshold, period_unit, period)
    slope = period_slope.det_slope(sample_df, "close")

    print(f"{threshold}, {period_unit}, {period} -> {slope}")

    assert slope.value == slope_status
