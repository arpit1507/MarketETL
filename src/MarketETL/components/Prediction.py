import os
import joblib
import pandas as pd
import numpy as np

from tensorflow.keras.models import load_model
from MarketETL.entity.config_entity import PredictionConfig

from MarketETL import logger


class Prediction:

    def __init__(self,config:PredictionConfig):
        self.config = config


    def forecast(self):

        df = pd.read_csv(
            self.config.transformed_data_file
        )

        results = []

        tickers = df["Ticker"].unique()

        for ticker in tickers:

            model = load_model(

                os.path.join(

                    self.config.trained_model_dir,

                    f"{ticker}.keras"
                ),
                compile=False
            )

            scaler = joblib.load(

                os.path.join(

                    self.config.scaler_dir,

                    f"{ticker}.pkl"
                )
            )

            stock_df = df[
                df["Ticker"] == ticker
            ].sort_values("Date")

            close_values = stock_df[
                ["Close"]
            ].values

            scaled = scaler.transform(
                close_values
            )

            last_window = scaled[
                -self.config.sequence_length:
            ]

            forecast = []

            for _ in range(
                self.config.forecast_days
            ):

                pred = model.predict(

                    last_window.reshape(
                        1,
                        self.config.sequence_length,
                        1
                    ),

                    verbose=0
                )

                forecast.append(
                    pred[0][0]
                )

                last_window = np.vstack(

                    [
                        last_window[1:],
                        pred
                    ]
                )

            forecast = scaler.inverse_transform(

                np.array(
                    forecast
                ).reshape(-1,1)
            )

            for value in forecast:

                results.append({

                    "Ticker": ticker,

                    "Predicted_Close":
                        float(value[0])
                })

        pd.DataFrame(
            results
        ).to_csv(

            self.config.forecast_file,

            index=False
        )

        logger.info(
            "Forecast saved"
        )