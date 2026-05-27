from MarketETL import logger

from MarketETL.components.data_loading import (
    DataLoading
)

from MarketETL.config.configuration import (
    ConfigurationManager
)


class DataLoadingPipeline:

    def __init__(self):
        pass

    def main(self):

        config = (
            ConfigurationManager()
        )

        data_loading_config = (
            config.get_data_loading_config()
        )

        loader = DataLoading(
            config=data_loading_config
        )

        loader.load_to_rds()


if __name__ == "__main__":

    STAGE_NAME = (
        "Data Loading Stage"
    )

    try:

        logger.info(
            f"{STAGE_NAME} started"
        )

        obj = DataLoadingPipeline()

        obj.main()

        logger.info(
            f"{STAGE_NAME} completed"
        )

    except Exception as e:
        logger.exception(e)
        raise e