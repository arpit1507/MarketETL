import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import os


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="MarketETL Dashboard",
    layout="wide"
)

st.title("📈 MarketETL Dashboard")


# ==========================
# DB CONNECTION
# ==========================

@st.cache_resource
def get_engine():

    connection_string = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
        f"?sslmode=verify-full"
        f"&sslrootcert="
        f"{os.getenv('SSL_ROOT_CERT')}"
    )

    return create_engine(connection_string)


engine = get_engine()


# ==========================
# LOAD STOCK DATA
# ==========================

@st.cache_data(ttl=3600)
def load_stock_data():

    query = '''
    SELECT *
    FROM stock_prices
    '''

    return pd.read_sql(
        query,
        engine
    )


# ==========================
# LOAD FORECAST
# ==========================

@st.cache_data(ttl=3600)
def load_forecast():

    forecast_df = pd.read_csv(
        "artifacts/predictions/forecast.csv"
    )

    # Get latest historical market date
    stock_df = load_stock_data()

    stock_df["Date"] = pd.to_datetime(
        stock_df["Date"],
        format="mixed"
    )

    last_market_date = stock_df["Date"].max()

    all_forecast_rows = []

    # Generate forecast dates per ticker
    for ticker in forecast_df["Ticker"].unique():

        ticker_forecast = forecast_df[
            forecast_df["Ticker"] == ticker
        ].copy()

        # Business days only (Mon-Fri)
        future_dates = pd.bdate_range(
            start=last_market_date + pd.Timedelta(days=1),
            periods=len(ticker_forecast)
        )

        ticker_forecast["Date"] = future_dates

        all_forecast_rows.append(
            ticker_forecast
        )

    final_forecast_df = pd.concat(
        all_forecast_rows,
        ignore_index=True
    )

    return final_forecast_df


df = load_stock_data()
forecast_df = load_forecast()
df["Date"] = pd.to_datetime(df["Date"], format="mixed")

# ==========================
# SIDEBAR
# ==========================

st.sidebar.header("Settings")

ticker = st.sidebar.selectbox(
    "Ticker",
    sorted(df["Ticker"].unique())
)

show_rsi = st.sidebar.checkbox(
    "Show RSI",
    value=True
)

show_volatility = st.sidebar.checkbox(
    "Show Volatility",
    value=True
)


# ==========================
# FILTER
# ==========================

ticker_df = df[
    df["Ticker"] == ticker
].copy()

ticker_forecast = forecast_df[
    forecast_df["Ticker"] == ticker
].copy()


# ==========================
# PRICE CHART
# ==========================

st.subheader(f"{ticker} Close Price")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ticker_df["Date"],
        y=ticker_df["Close"],
        name="Close"
    )
)

fig.add_trace(
    go.Scatter(
        x=ticker_df["Date"],
        y=ticker_df["MA_7"],
        name="MA 7"
    )
)

fig.add_trace(
    go.Scatter(
        x=ticker_df["Date"],
        y=ticker_df["MA_30"],
        name="MA 30"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================
# FORECAST
# ==========================

st.subheader("🔮 Forecast")

forecast_fig = go.Figure()

forecast_fig.add_trace(
    go.Scatter(
        x=ticker_df["Date"],
        y=ticker_df["Close"],
        name="Actual"
    )
)

forecast_fig.add_trace(
    go.Scatter(
        x=ticker_forecast["Date"],
        y=ticker_forecast["Predicted_Close"],
        name="Predicted"
    )
)

st.plotly_chart(
    forecast_fig,
    use_container_width=True
)


# ==========================
# METRICS
# ==========================

col1, col2, col3 = st.columns(3)

latest_close = ticker_df["Close"].iloc[-1]

col1.metric(
    "Latest Close",
    round(latest_close, 2)
)

latest_rsi = ticker_df["RSI"].iloc[-1]

col2.metric(
    "RSI",
    round(latest_rsi, 2)
)

latest_vol = ticker_df["Volatility"].iloc[-1]

col3.metric(
    "Volatility",
    round(latest_vol, 4)
)


# ==========================
# RSI CHART
# ==========================

if show_rsi:

    st.subheader("RSI")

    rsi_fig = px.line(
        ticker_df,
        x="Date",
        y="RSI"
    )

    st.plotly_chart(
        rsi_fig,
        use_container_width=True
    )


# ==========================
# VOLATILITY
# ==========================

if show_volatility:

    st.subheader("Volatility")

    vol_fig = px.line(
        ticker_df,
        x="Date",
        y="Volatility"
    )

    st.plotly_chart(
        vol_fig,
        use_container_width=True
    )


# ==========================
# TABLE
# ==========================

st.subheader("Latest Data")

st.dataframe(
    ticker_df.tail(10)
)

# ==========================
# AUTO INSIGHTS
# ==========================

st.subheader("🧠 AI Insights")

latest_close = ticker_df["Close"].iloc[-1]
latest_ma7 = ticker_df["MA_7"].iloc[-1]
latest_ma30 = ticker_df["MA_30"].iloc[-1]
latest_rsi = ticker_df["RSI"].iloc[-1]
latest_vol = ticker_df["Volatility"].iloc[-1]

forecast_start = ticker_forecast["Predicted_Close"].iloc[0]
forecast_end = ticker_forecast["Predicted_Close"].iloc[-1]

forecast_change = (
    (forecast_end - forecast_start)
    / forecast_start
) * 100

insights = []

# ==========================
# TREND ANALYSIS
# ==========================

if latest_ma7 > latest_ma30:
    insights.append(
        "📈 Short-term trend is bullish "
        "(MA 7 is above MA 30)."
    )
else:
    insights.append(
        "📉 Short-term trend is bearish "
        "(MA 7 is below MA 30)."
    )

# ==========================
# RSI ANALYSIS
# ==========================

if latest_rsi > 70:
    insights.append(
        "⚠️ Stock may be overbought "
        f"(RSI: {latest_rsi:.2f})."
    )

elif latest_rsi < 30:
    insights.append(
        "🟢 Stock may be oversold "
        f"(RSI: {latest_rsi:.2f})."
    )

else:
    insights.append(
        f"✅ RSI is in a neutral range "
        f"({latest_rsi:.2f})."
    )

# ==========================
# VOLATILITY
# ==========================

if latest_vol > 0.05:
    insights.append(
        "🔥 High volatility detected."
    )

elif latest_vol < 0.02:
    insights.append(
        "😌 Low volatility observed."
    )

else:
    insights.append(
        "📊 Moderate volatility levels."
    )

# ==========================
# FORECAST ANALYSIS
# ==========================

if forecast_change > 5:
    insights.append(
        f"🚀 Forecast predicts a strong upside "
        f"of {forecast_change:.2f}%."
    )

elif forecast_change > 0:
    insights.append(
        f"📈 Forecast predicts a mild gain "
        f"of {forecast_change:.2f}%."
    )

elif forecast_change < -5:
    insights.append(
        f"🔻 Forecast predicts a significant drop "
        f"of {abs(forecast_change):.2f}%."
    )

else:
    insights.append(
        f"📉 Forecast predicts a slight decline "
        f"of {abs(forecast_change):.2f}%."
    )

# ==========================
# DISPLAY INSIGHTS
# ==========================

for insight in insights:
    st.info(insight)