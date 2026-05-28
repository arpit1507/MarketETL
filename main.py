from MarketETL.pipeline.DataExtractionPipeline import (DataExtractionPipeline)

from MarketETL.pipeline.DataTransformationPipeline import (DataTransformationPipeline)

from MarketETL.pipeline.DataLoadingPipeline import (DataLoadingPipeline)

from MarketETL.pipeline.ModelTrainingPipeline import (ModelTrainingPipeline)

from MarketETL.pipeline.PredictionPipeline import (PredictionPipeline)

def main():

    DataExtractionPipeline().main()

    DataTransformationPipeline().main()

    DataLoadingPipeline().main()

    ModelTrainingPipeline().main()

    PredictionPipeline().main()

if __name__=="__main__":
    main()