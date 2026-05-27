# MarketETL

## Aim

**MarketETL** is an end-to-end stock market ETL pipeline built in Python using modern data engineering practices.

The objective of the project is to design a scalable and production-style workflow for extracting stock market data, transforming it into analytics-ready datasets, storing it in cloud databases, and preparing it for forecasting and dashboard applications.

The project focuses on:

* Extracting historical stock market data using Yahoo Finance through the Python `yfinance` API
* Cleaning and validating raw financial datasets
* Transforming stock data into analytics-ready format
* Engineering financial indicators:

  * Moving Average (7-day / 30-day)
  * Daily Returns
  * Rolling Volatility
  * RSI (Relative Strength Index)
* Loading processed data into PostgreSQL hosted on Amazon RDS
* Building modular ETL pipelines
* Managing configuration using YAML
* Logging each pipeline stage
* Performing incremental database loading (append only new records / prevent duplicates)
* Preparing structured stock data for:

  * dashboards
  * analytics
  * time-series forecasting
  * machine learning workflows

This project simulates a real-world financial data engineering system and demonstrates practical experience in:

* ETL pipeline development
* Data engineering
* Cloud database integration
* Data transformation
* Pipeline automation
* Configuration management
* Logging and monitoring
* Financial analytics
* Scalable Python project architecture

---

# Project Workflow

```text
Yahoo Finance API
        ↓
Data Extraction
        ↓
Data Validation
        ↓
Feature Engineering
        ↓
Transformation
        ↓
AWS RDS PostgreSQL
        ↓
Incremental Loading
        ↓
Forecasting / Dashboard
```

---

# Project Structure

```bash
MarketETL/
│
├── config/
│   ├── config.yaml
│   └── schema.yaml
│
├── logs/
│   └── running_logs.log
│
├── artifacts/
│   ├── data_ingestion/
│   ├── transformation/
│   ├── model/
│
├── src/
│   └── MarketETL/
│       │
│       ├── components/
│       │   ├── data_extraction.py
│       │   ├── data_transformation.py
│       │   └── data_loading.py
│       │
│       ├── config/
│       │   └── configuration.py
│       │
│       ├── constants/
│       │
│       ├── entity/
│       │   └── config_entity.py
│       │
│       ├── pipeline/
│       │   ├── DataExtractionPipeline.py
│       │   ├── DataTransformationPipeline.py
│       │   └── DataLoadingPipeline.py
│       │
│       ├── utils/
│       │
│       └── __init__.py
│
├── templates/
│
├── params.yaml
├── requirements.txt
├── setup.py
├── main.py
└── README.md
```

---

# Steps followed in the project

## 1. Entity Design

Created dataclass-based configuration entities:

* `DataExtractionConfig`
* `DataTransformationConfig`
* `DataLoadingConfig`

Purpose:

* type-safe config handling
* reusable configuration objects
* clean modular architecture

Example:

```python
@dataclass(frozen=True)
class DataExtractionConfig:
```

---

## 2. Configuration Manager

Created a centralized `ConfigurationManager`

Responsibilities:

* read YAML config
* read params
* read schema
* create artifact folders
* pass config objects to pipelines

Files:

```bash
configuration.py
config.yaml
params.yaml
schema.yaml
```

---

## 3. Data Extraction Component

Built extraction component using `yfinance`

Features:

* multiple ticker download
* configurable date range
* configurable interval
* auto-adjust prices
* combine stock data into one dataset
* save raw CSV

Example tickers:

```text
AAPL
MSFT
TSLA
NVDA
GOOGL
```

Output:

```bash
artifacts/data_ingestion/stock_data.csv
```

---

## 4. Data Transformation Component

Built transformation module

Applied:

* Daily return calculation
* 7-day moving average
* 30-day moving average
* rolling volatility
* RSI indicator
* missing value handling

Output:

```bash
artifacts/transformation/processed_stock_data.csv
```

Final columns:

```text
Date
Close
High
Low
Open
Volume
Ticker
Daily_Return
MA_7
MA_30
Volatility
RSI
```

---

## 5. Data Loading Pipeline

Loaded transformed stock data into:

PostgreSQL on Amazon RDS

Features:

* secure connection
* SSL certificate verification
* `SQLAlchemy + psycopg2`
* automatic table creation
* append mode
* duplicate prevention using:

```text
(Date + Ticker)
```

Incremental loading:

```text
insert only new rows
skip duplicates
```

---

## 6. Logging

Implemented logging across all pipelines

Tracks:

* pipeline start
* config loading
* data download
* transformation status
* database loading
* errors / exceptions

Example:

```text
INFO: Data Loading Stage started
INFO: Rows loaded to PostgreSQL
```

---

## 7. Pipeline Architecture

Each ETL stage runs independently

Pipelines:

```bash
DataExtractionPipeline.py
DataTransformationPipeline.py
DataLoadingPipeline.py
```

Benefits:

* reusable
* modular
* production-ready structure

---

## 8. Forecasting Ready

Prepared transformed data for time-series forecasting:

Future additions:

* LSTM forecasting
* Prophet forecasting
* dashboard visualization
* scheduled ETL
* AWS deployment automation

---

# Installation

Create environment:

```bash
conda create -n MarketETL python=3.9 -y
```

Activate:

```bash
conda activate MarketETL
```

Install:

```bash
pip install -r requirements.txt
```

---

# Libraries Used

Core:

* numpy
* pandas
* scipy

Finance:

* yfinance

Database:

* psycopg2
* sqlalchemy

Configuration:

* PyYAML
* python-box
* ensure

Utilities:

* tqdm
* joblib

Visualization:

* streamlit
* seaborn

Development:

* dvc
* types-PyYAML


