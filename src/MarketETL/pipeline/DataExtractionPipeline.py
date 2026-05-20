from MarketETL.components.data_extraction import DataExtraction
from MarketETL.config.configuration import ConfigurationManager
from MarketETL import logger

class DataExtractionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config_manager = ConfigurationManager()
            data_extraction_config = (
                config_manager.get_data_extraction_config()
            )
            data_extraction = DataExtraction(
                config=data_extraction_config
            )
            data_extraction.download_stock_data()
    
        except Exception as e:
            logger.exception(e)
            raise e
        
if __name__== "__main__":
    stage_name="Data Extraction"
    try:
        logger.info(f">>>>>> Stage {stage_name} started <<<<<<")

        obj = DataExtractionPipeline()

        obj.main()

        logger.info(f">>>>>> Stage {stage_name} completed <<<<<<")

    except Exception as e:
        logger.exception(e)
        raise e
