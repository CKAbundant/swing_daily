"""Test scripts for 'GenData' class."""

from pprint import pformat

from strat_backtest.utils import load_parquet

from src.gen_data import GenData
from tests.utils.test_utils import list_datatype


def test_append_ta(sample_df):
    """Test if required ta are appended correctly to DataFrame"""

    # TA indicators to be appended
    ta_dict = {
        "sma_20": {"data": ["close"], "timeperiod": 20},
        "sma_40": {"data": ["close"], "timeperiod": 40},
        "cci_5": {"data": ["high", "low", "close"], "timeperiod": 5},
        "atr_14": {"data": ["high", "low", "close"], "timeperiod": 14},
    }

    print(f"ta_dict : \n{pformat(ta_dict, sort_dicts=False)}\n")

    gen_data = GenData(ta_dict)
    df = gen_data(sample_df)
    print(f"\n\n{df}\n")
