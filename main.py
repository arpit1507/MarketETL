from src.MarketETL import logger
from src.MarketETL.utils.common import read_yaml
from pathlib import Path
logger.info("Starting a new Project")
yaml_file=Path("/Users/arpitagrawal/Desktop/Resume Projects/MarketETL/config/config.yaml")
read_yaml(yaml_file)