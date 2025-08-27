"""Test scripts for 'GenData' class."""

from strat_backtest.utils import load_parquet


def test_append_ta(sample_df):
    """Test if required ta are appended correctly to DataFrame"""

    # df = load_parquet("./tests/data/sample.parquet")
    # print(f"\n\n{df}\n")

    print(f"\n\n{sample_df}\n")
