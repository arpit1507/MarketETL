import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import text
from urllib.parse import quote_plus

from MarketETL import logger
from MarketETL.entity.config_entity import (
    DataLoadingConfig
)


class DataLoading:

    def __init__(
        self,
        config: DataLoadingConfig
    ):
        self.config = config

    def load_to_rds(self):

        try:

            logger.info(
                "Reading transformed CSV"
            )

            df = pd.read_csv(
                self.config.transformed_data_file
            )

            # -------------------
            # schema validation
            # -------------------

            missing_cols = [
                col
                for col in
                self.config.columns.keys()
                if col not in df.columns
            ]

            if missing_cols:
                raise ValueError(
                    f"Missing columns: "
                    f"{missing_cols}"
                )

            logger.info(
                f"Rows in CSV: {df.shape[0]}"
            )

            # -------------------
            # DB connection
            # -------------------

            host = self.config.DB_HOST
            port = self.config.DB_PORT
            db = self.config.DB_NAME
            user = self.config.DB_USER

            password = quote_plus(
                self.config.DB_PASSWORD
            )

            cert = self.config.SSL_ROOT_CERT

            connection_string = (
                f"postgresql+psycopg2://"
                f"{user}:{password}"
                f"@{host}:{port}/{db}"
                f"?sslmode=verify-full"
                f"&sslrootcert={cert}"
            )

            logger.info(
                "Connecting to AWS RDS"
            )

            engine = create_engine(
                connection_string
            )

            # -------------------
            # fetch existing keys
            # -------------------

            existing_df = pd.read_sql(
                text(
                    '''
                    SELECT "Date","Ticker"
                    FROM stock_prices
                    '''
                ),
                engine
            )

            # normalize date format
            df["Date"] = pd.to_datetime(
                df["Date"]
            )

            existing_df["Date"] = pd.to_datetime(
                existing_df["Date"]
            )

            # -------------------
            # remove duplicates
            # -------------------

            merged = df.merge(
                existing_df,
                on=["Date","Ticker"],
                how="left",
                indicator=True
            )

            new_rows = merged[
                merged["_merge"] == "left_only"
            ].drop(
                columns=["_merge"]
            )

            logger.info(
                f"New rows to insert: "
                f"{new_rows.shape[0]}"
            )

            # -------------------
            # append only new rows
            # -------------------

            if not new_rows.empty:

                new_rows.to_sql(
                    name=self.config.table_name,
                    con=engine,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=1000
                )

                logger.info(
                    "Only new rows inserted"
                )

            else:

                logger.info(
                    "No new rows found"
                )

        except Exception as e:

            logger.exception(e)

            raise e