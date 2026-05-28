from MarketETL import logger

from MarketETL.config.configuration import (
    ConfigurationManager
)

from MarketETL.components.Prediction import (
    Prediction
)


STAGE_NAME = "Prediction"


class PredictionPipeline:

    def __init__(self):
        pass


    def main(self):

        try:

            config = (
                ConfigurationManager()
            )

            prediction_config = (
                config.get_prediction_config()
            )

            predictor = Prediction(
                config=prediction_config
            )

            predictor.forecast()

        except Exception as e:

            logger.exception(e)

            raise e


if __name__ == "__main__":

    try:

        logger.info(
            f"{STAGE_NAME} Stage started"
        )

        obj = PredictionPipeline()

        obj.main()

        logger.info(
            f"{STAGE_NAME} Stage completed"
        )

    except Exception as e:

        logger.exception(e)

        raise e