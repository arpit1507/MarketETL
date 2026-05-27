from MarketETL.constants import config_file_path,params_file_path,schema_file_path
from MarketETL.utils.common import read_yaml,create_directories
from MarketETL.entity.config_entity import (DataExtractionConfig,DataTransfromationConfig,DataLoadingConfig)

class ConfigurationManager:
    def __init__(self, config_file_path=config_file_path, params_file_path=params_file_path):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        self.schema = read_yaml(schema_file_path)
        create_directories([self.config.artifacts_root])

    def get_data_extraction_config(self) -> DataExtractionConfig:
        config=self.config.Data_extraction
        params=self.params.data_extraction
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

    def get_data_transformation_config(self) -> DataTransfromationConfig:
        config=self.config.Data_Transformation
        params=self.params.data_transformation
        create_directories([config.root_dir])

        return DataTransfromationConfig(
            root_dir=config.root_dir,
            raw_data_file= self.config.Data_extraction.local_data_file,
            transformed_data_file=config.transformed_data_file,
            rolling_window_7=params.rolling_window_7,
            rolling_window_30=params.rolling_window_30,
            calculate_daily_return=params.calculate_daily_return,
            calculate_volatility=params.calculate_volatility,
            calculate_rsi=params.calculate_rsi,
            missing_value_strategy=params.missing_value_strategy
        )

    def get_data_loading_config(self) -> DataLoadingConfig:

        config = self.config.Data_Loading
        params = self.params.database
        schema = self.schema.COLUMNS

        return DataLoadingConfig(

            transformed_data_file=(
                self.config
                .Data_Transformation
                .transformed_data_file
            ),

            DB_HOST=config.DB_HOST,
            DB_PORT=config.DB_PORT,
            DB_NAME=config.DB_NAME,
            DB_USER=config.DB_USER,
            DB_PASSWORD=config.DB_PASSWORD,
            SSL_ROOT_CERT=config.SSL_ROOT_CERT,

            table_name=params.table_name,
            if_exists=params.if_exists,

            columns=schema
        )