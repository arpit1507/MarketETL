import os
import joblib
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    LSTM,
    Dense,
    Dropout
)

from MarketETL import logger


class ModelTraining:

    def __init__(self, config):
        self.config = config


    def create_sequences(
        self,
        values
    ):

        X = []
        y = []

        seq_len = self.config.sequence_length

        for i in range(
            seq_len,
            len(values)
        ):

            X.append(
                values[
                    i-seq_len:i
                ]
            )

            y.append(
                values[i]
            )

        return (
            np.array(X),
            np.array(y)
        )


    def build_model(self):

        model = Sequential()

        model.add(
            LSTM(
                64,
                return_sequences=True,
                input_shape=(
                    self.config.sequence_length,
                    1
                )
            )
        )

        model.add(
            Dropout(0.2)
        )

        model.add(
            LSTM(32)
        )

        model.add(
            Dense(1)
        )

        model.compile(
            optimizer="adam",
            loss="mse"
        )

        return model


    def train(self):

        df = pd.read_csv(
            self.config.transformed_data_file
        )

        tickers = df[
            "Ticker"
        ].unique()

        for ticker in tickers:

            logger.info(
                f"Training {ticker}"
            )

            stock_df = df[
                df["Ticker"] == ticker
            ].copy()

            stock_df = stock_df.sort_values(
                "Date"
            )

            values = stock_df[
                [self.config.target_column]
            ].values

            scaler = MinMaxScaler()

            scaled_values = scaler.fit_transform(
                values
            )

            X, y = self.create_sequences(
                scaled_values
            )

            model = self.build_model()

            model.fit(

                X,
                y,

                epochs=
                    self.config.epochs,

                batch_size=
                    self.config.batch_size,

                validation_split=
                    self.config.validation_split,

                verbose=1
            )

            model.save(

                os.path.join(

                    self.config.trained_model_dir,

                    f"{ticker}.keras"
                )
            )

            joblib.dump(

                scaler,

                os.path.join(

                    self.config.scaler_dir,

                    f"{ticker}.pkl"
                )
            )

            logger.info(
                f"{ticker} trained"
            )