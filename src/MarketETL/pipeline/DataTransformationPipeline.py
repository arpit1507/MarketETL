from MarketETL.components.data_transformation import (DataTransformation)

from MarketETL.config.configuration import (ConfigurationManager)

from MarketETL import logger


class DataTransformationPipeline:

    def __init__(self):
        pass

    def main(self):

        try:

            config = (
                ConfigurationManager()
            )

            transformation_config = (
                config.get_data_transformation_config()
            )

            data_transformation = (
                DataTransformation(
                    config=transformation_config
                )
            )

            data_transformation.transform_stock_data()

        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == "__main__":

    STAGE_NAME = "Data Transformation Stage"

    try:

        logger.info(
            f">>>>>> {STAGE_NAME} started <<<<<<"
        )

        obj = DataTransformationPipeline()

        obj.main()

        logger.info(
            f">>>>>> {STAGE_NAME} completed <<<<<<"
        )

    except Exception as e:
        logger.exception(e)
        raise e