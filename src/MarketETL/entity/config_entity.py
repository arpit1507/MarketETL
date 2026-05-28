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

    table_name: str
    if_exists: str

    columns: dict


@dataclass(frozen=True)
class ModelTrainingConfig:
    root_dir: Path
    trained_model_dir: Path
    scaler_dir: Path
    transformed_data_file: Path
    sequence_length: int
    epochs: int
    batch_size: int
    validation_split: float
    target_column: str
    forecast_days: int

@dataclass(frozen=True)
class PredictionConfig:
    root_dir: Path
    forecast_file: Path
    transformed_data_file: Path
    trained_model_dir: Path
    scaler_dir: Path
    sequence_length: int
    forecast_days: int