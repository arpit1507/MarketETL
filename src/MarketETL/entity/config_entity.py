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

    
