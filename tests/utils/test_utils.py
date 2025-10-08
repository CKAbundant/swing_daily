"""Utility functions used in testing"""

import pandas as pd


def list_datatype(df: pd.DataFrame, df_name: str = "df") -> None:
    """List unique datatypes for each column in DataFrame."""

    print(f"\n'{df_name}' DataFrame")
    print("-" * 20)

    for col in df:
        # Get unique datatypes for each column
        unique_list = list(set([type(var) for var in df[col]]))

        print(f"{col:<10} : {unique_list}")

    print()
