from MarketETL.constants import config_file_path,params_file_path,schema_file_path
from MarketETL.utils.common import read_yaml,create_directories
from MarketETL.entity.config_entity import DataExtractionConfig

class ConfigurationManager:
    def __init__(self, config_file_path=config_file_path, params_file_path=params_file_path):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        self.schema = read_yaml(schema_file_path)
        create_directories([self.config.artifacts_root])

    def get_data_extraction_config(self) -> DataExtractionConfig:
        config=self.config.Data_ingestion
        params=self.params.data_ingestion
        create_directories([config.root_dir])
        
        return DataExtractionConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            tickers=params.tickers,
            start_date=params.start_date,
            end_date=params.end_date,
            interval=params.interval,
            auto_adjust=params.auto_adjust
        )
