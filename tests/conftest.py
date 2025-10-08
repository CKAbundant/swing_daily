"""All fixtures automatically available for testing"""

from pathlib import Path

import pytest
from strat_backtest.utils import load_parquet

FIXTURE_DIR = Path(__file__).parent


@pytest.fixture
def sample_df():
    """Load 'sample.parquet' as fixture."""

    parquet_path = FIXTURE_DIR.joinpath("data", "sample.parquet")
    print(f"{parquet_path=}")

    if not parquet_path.is_file():
        raise FileNotFoundError(
            f"sample.parquet doesn't exist at '{parquet_path.as_posix()}'"
        )

    return load_parquet(parquet_path)
