from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class DataExtractionConfig:
    root_dir: Path
    tickers: List[str]
    local_data_file: Path
    start_date: str
    end_date: str
    interval: str
    auto_adjust: bool

@dataclass(frozen=True)
class DataTransfromationConfig:
    root_dir: Path
    raw_data_file: Path
    transformed_data_file: Path
    rolling_window_7: int
    rolling_window_30: int
    calculate_daily_return: bool
    calculate_volatility: bool
    calculate_rsi: bool
    missing_value_strategy: str


@dataclass(frozen=True)
class DataLoadingConfig:

    transformed_data_file: Path

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SSL_ROOT_CERT: str

    table_name: str
    if_exists: str

    columns: dict
