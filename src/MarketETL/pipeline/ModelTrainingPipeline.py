from MarketETL import logger

from MarketETL.config.configuration import (
    ConfigurationManager
)

from MarketETL.components.Model_training import (
    ModelTraining
)


STAGE_NAME = "Model Training"


class ModelTrainingPipeline:

    def main(self):

        config = ConfigurationManager()

        training_config = (
            config.get_model_training_config()
        )

        trainer = ModelTraining(
            training_config
        )

        trainer.train()


if __name__ == "__main__":

    try:

        logger.info(
            f"{STAGE_NAME} started"
        )

        obj = ModelTrainingPipeline()

        obj.main()

        logger.info(
            f"{STAGE_NAME} completed"
        )

    except Exception as e:
        raise e