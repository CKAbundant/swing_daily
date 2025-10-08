"""Append TA indicators (using default settings) to OHLCV DataFrame:

1) cci
2) 20_ma
3) 40_ma
4) atr
"""

from typing import Any

import pandas as pd
import talib
from strat_backtest.utils import set_datetime, set_decimal_type


class GenData:
    """Append TA indicators to OHLCV DataFrame.

    Args:
        ta_dict (dict[str, dict[str, Any]]):
            Dictionary mapping technical indicators to their settings in ta-lib.

    Attributes:
        ta_dict (dict[str, dict[str, Any]]):
            Dictionary mapping technical indicators to their settings in ta-lib.
    """

    def __init__(self, ta_dict: dict[str, dict[str, Any]]):
        self.ta_dict = ta_dict

    def __call__(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Append TA indicators to OHLCV DataFrame based on 'ta_dict'.

        Args:
            data (pd.DataFrame): DataFrame containing OHLCV info of specific stock.

        Returns:
            df (pd.DataFrame): DataFrame with TA appended.
        """

        # Format DataFrame
        df = self.format_df(data)

        for col_name, params in self.ta_dict.items():
            # Get function name used in talib after validation
            self._validate_params(params, df)
            fn_name = self._get_fn_name(col_name)

            # Update input parameters required for talib computation
            params = self._update_params(fn_name, params, df)

            # Get ta values
            ta_indicator = getattr(talib, fn_name)
            ta_values = ta_indicator(**params)
            print(f"\n\n{ta_values=}")

            # Generate column name and append ta values to DataFrame
            df[col_name] = ta_values

        return df

    def _get_fn_name(self, col_name: str) -> str:
        """Get function name for talib computation from column name."""

        return col_name.split("_")[0].upper()

    def _validate_params(self, params: dict[str, Any], df: pd.DataFrame) -> None:
        """Validate 'params' contains 'data' key and price levels are found
        in DataFrame.

        Args:
            params (dict[str, Any]):
                Dictionary containing required input array and parameters for talib.
            df (pd.DataFrame):
                OHLCV dataframe for ta computation.

        Returns:
            None.
        """

        if "data" not in params:
            raise ValueError("'data' key missing!")

        if any(price_level not in df.columns for price_level in params["data"]):
            raise ValueError(
                "Not all price levels specified in 'data' key are columns in DataFrame"
            )

    def _update_params(
        self,
        fn_name: str,
        params: dict[str, Any],
        df: pd.DataFrame,
    ) -> dict[str, Any]:
        """Update input parameters required for talib computation by
        extracting relevant price levels from DataFrame.

        Args:
            fn_name (str):
                Function name used in talib computation.
            params (dict[str, Any]):
                Dictionary containing required input array and parameters for talib.
            df (pd.DataFrame):
                OHLCV dataframe for ta computation.

        Returns:
            df (pd.DataFrame): DataFrame with appended ta.
        """

        updated_params = {}

        for var, value in params.items():
            if var == "data":
                # Extract price levels from DataFrame
                # E.g. {"data": ["high", "low", "close"]}
                updated_params.update(self._get_input_array(fn_name, value, df))
            else:
                updated_params[var] = value

        return updated_params

    def _get_input_array(
        self, fn_name: str, input_list: list[str], df: pd.DataFrame
    ) -> dict[str, Any]:
        """Get dictionary mapping correct input variable used in talib to price levels.

        Args:
            fn_name (str):
                Function name used in talib computation.
            input_list (list[str]):
                List of required price levels e.g. 'high', 'low', etc.
            df (pd.DataFrame):
                OHLCV dataframe for ta computation.

        Returns:
            params (dict[str, Any]): Update parameters with actual price levels.
        """

        params = {}

        for price_level in input_list:
            var = "real" if fn_name == "SMA" else price_level
            params[var] = df[price_level]

        return params

    def format_df(self, data: pd.DataFrame) -> pd.DataFrame:
        """Format DataFrame:

        - Lowercase column names
        - Ensure columns in ticker followed by OHLCV order.
        - Ensure date is set as a column instead of index.
        """

        df = data.copy()

        # Reset index if index has assigned name
        if df.index.name is not None:
            df = df.reset_index()

        # Set date-related column to datetime type
        df = set_datetime(df)

        # Lowercase columns
        df.columns = [col.lower() for col in df.columns]

        if "date" not in df.columns:
            raise ValueError("'date' column is missing!")

        req_cols = ["date", "open", "high", "low", "close", "volume"]

        # Ensure columns in ticker followed by OHLCV order
        if "ticker" in df.columns:
            req_cols.insert(1, "ticker")

        df = df.loc[:, req_cols]

        # Set numeric columns to Decimal type
        df = set_decimal_type(df)

        return df
