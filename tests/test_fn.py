from pathlib import Path

import numpy as np
import pandas as pd
import talib

from tests.utils.test_utils import list_datatype


def test_fn():
    b = {"b": 1, "c": 2, "d": 3}
    a = {}
    a.update(b)

    print(a)
