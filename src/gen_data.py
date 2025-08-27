"""Append TA indicators (using default settings) to OHLCV DataFrame:

1) cci
2) 20_ma
3) 40_ma
4) atr
"""

from typing import Any

import pandas as pd
from strat_backtest.utils import convert_to_decimal, set_datetime, set_decimal_type


class GenData:
    """Append TA indicators to OHLCV DataFrame.

    Args:
        ta_dict (dict[str, tuple[Any]]):
            Dictionary mapping technical indicators to their settings in ta-lib.

    Attributes:
        ta_dict (dict[str, tuple[Any]]):
            Dictionary mapping technical indicators to their settings in ta-lib.
    """

    def __init__(self, ta_dict: dict[str, tuple[Any]]):
        self.ta_dict = ta_dict

    def append_ta(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Append TA indicators to OHLCV DataFrame based on 'ta_dict'.

        Args:
            df (pd.DataFrame): DataFrame containing OHLCV info of specific stock.

        Returns:
            df (pd.DataFrame): DataFrame with TA appended.
        """

        df = self.format_df(df)

        return df

    def format_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format DataFrame:

        - Lowercase column names
        - Ensure columns in ticker followed by OHLCV order.
        - Ensure date is set as a column instead of index.
        """

        # Reset index if index has assigned name
        if df.index.name is not None:
            df = df.reset_index()

        # Set date-related column to datetime type
        df = set_datetime(df)

        # Lowercase columns
        df.columns = [col.lower() for col in df.columns]

        if "date" not in df.columns:
            raise ValueError("'date' column is missing!")

        ohlcv_col = ["date", "open", "high", "low", "close", "volume"]

        # Ensure columns in ticker followed by OHLCV order
        if "ticker" not in df.columns:
            df = df.loc[:, ohlcv_col]
        else:
            df = df.loc[: ["ticker"] + ohlcv_col]

        # Set numeric columns to Decimal type
        df = set_decimal_type(df)

        return df
