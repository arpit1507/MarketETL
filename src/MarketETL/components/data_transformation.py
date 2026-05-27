from MarketETL import logger
from MarketETL.entity.config_entity import DataTransfromationConfig

import pandas as pd
import numpy as np



class DataTransformation:

    def __init__(self, config: DataTransfromationConfig):
        self.config = config

    def transform_stock_data(self):

        try:

            logger.info("Reading raw stock data")

            df = pd.read_csv(self.config.raw_data_file)

            logger.info(f"Raw dataframe shape: {df.shape}")
            

            # =========================
            # CONVERT DATE COLUMN
            # =========================

            logger.info("Converting Date column")

            df["Date"] = pd.to_datetime(df["Date"])

            # =========================
            # SORT VALUES
            # =========================

            logger.info("Sorting values")

            df.sort_values(
                by=["Ticker", "Date"],
                inplace=True
            )

            # =========================
            # DAILY RETURNS
            # =========================

            logger.info("Calculating daily returns")

            df["Daily_Return"] = (
                df.groupby("Ticker")["Close"]
                .pct_change()
            )

            # =========================
            # MOVING AVERAGES
            # =========================

            logger.info("Calculating moving averages")

            df["MA_7"] = (
                df.groupby("Ticker")["Close"]
                .transform(
                    lambda x: x.rolling(
                        window=self.config.rolling_window_7
                    ).mean()
                )
            )

            df["MA_30"] = (
                df.groupby("Ticker")["Close"]
                .transform(
                    lambda x: x.rolling(
                        window=self.config.rolling_window_30
                    ).mean()
                )
            )

            # =========================
            # VOLATILITY
            # =========================

            logger.info("Calculating volatility")

            df["Volatility"] = (
                df.groupby("Ticker")["Daily_Return"]
                .transform(
                    lambda x: x.rolling(window=7).std()
                )
            )

            # =========================
            # RSI CALCULATION
            # =========================

            logger.info("Calculating RSI")

            delta = df.groupby("Ticker")["Close"].diff()

            gain = delta.clip(lower=0)

            loss = -1 * delta.clip(upper=0)

            avg_gain = (
                gain.groupby(df["Ticker"])
                .transform(
                    lambda x: x.rolling(14).mean()
                )
            )

            avg_loss = (
                loss.groupby(df["Ticker"])
                .transform(
                    lambda x: x.rolling(14).mean()
                )
            )

            rs = avg_gain / avg_loss

            df["RSI"] = 100 - (100 / (1 + rs))

            # =========================
            # FINAL CLEANING
            # =========================

            logger.info("Final cleaning")

            df.dropna(inplace=True)

            # =========================
            # SAVE PROCESSED DATA
            # =========================

            logger.info("Saving transformed data")

            df.to_csv(
                self.config.transformed_data_file,
                index=False
            )

            logger.info(
                f"Processed data saved at: "
                f"{self.config.transformed_data_file}"
            )

            logger.info(
                f"Final dataframe shape: {df.shape}"
            )

            return df

        except Exception as e:
            logger.exception(e)
            raise e