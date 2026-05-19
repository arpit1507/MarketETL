import logging

message='%(asctime)s : %(levelname)s : %(module)s : %(message)s'

logging.basicConfig(level=logging.INFO, format=message)

logger = logging.getLogger("MarketETL_logger")

