from MarketETL.config.configuration import DataExtractionConfig
from MarketETL import logger
import yfinance as yf
import pandas as pd
from datetime import date
class DataExtraction:

    def __init__(self, config: DataExtractionConfig):
        self.config = config

    def download_stock_data(self):
        all_data = []

        end_date = (
            self.config.end_date
            if self.config.end_date
                else date.today().strftime("%Y-%m-%d")
        )

        for ticker in self.config.tickers:

            df = yf.download(
                ticker,
                start=self.config.start_date,
                end=end_date,
                interval=self.config.interval,
                auto_adjust=self.config.auto_adjust
            )

            # Reset index
            df.reset_index(inplace=True)

            # Flatten multi-index columns
            df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

            # Add ticker column
            df["Ticker"] = ticker

            all_data.append(df)
            

        final_df = pd.concat(all_data, ignore_index=True)

        final_df.to_csv(self.config.local_data_file, index=False)

        logger.info(f"Data saved at: {self.config.local_data_file}")

        return final_df
    
