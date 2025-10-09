"""Trading system constants and enumerations.

This module contains Enum classes and Literal type constants
used throughout the 'swing_daily' repo.
"""

from enum import Enum
from typing import Literal

# # Static variables
# OhlcType = Literal["open", "high", "low", "close"]


# Dynamic variables
class SlopeStatus(Enum):
    up = 1
    sideway = 0
    down = -1
