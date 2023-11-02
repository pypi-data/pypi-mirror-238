import pandas as pd
from os import environ

# -----------------------------------------
# 1. Read and transform data
# -----------------------------------------

# Read data
active_positions_filename = "/Users/johnreese/Downloads/delphia-am-prod_DCMF-august-release-2023-07-25-v013-monthly_daily_positions_output_active_portfolio_full_daily_positions.parquet"
active_attributed_returns_filename = "/Users/johnreese/Downloads/delphia-am-prod_DCMF-august-release-2023-07-25-v013-monthly_reports_output_active_portfolio_attributed_returns.parquet"

df_weights_starting = pd.read_parquet(active_positions_filename)
df_attr_returns = pd.read_parquet(active_attributed_returns_filename)

# Pivot holdings into expected format
df_weights_starting = (
    df_weights_starting["weight"]
    .reset_index()
    .pivot(index="date", columns="company_id", values="weight")
    .fillna(0)
)

# Calculate ending weights
df_weights_ending = df_weights_starting.shift(-1)

# Calculate trades (WHICH SEEM TO HAPPEN AFTER ATTR RETURNS)
df_attr_returns_pivoted = (
    df_attr_returns.reset_index()
    .pivot(index="date", columns="company_id", values="returns")
    .fillna(0)
)

# Trades
df_trades = df_weights_ending - df_attr_returns_pivoted - df_weights_starting

# Calculate returns by company (note: trades happen after attr returns)
df_returns = df_attr_returns_pivoted / df_weights_starting
df_returns = df_returns.fillna(0)

# -----------------------------------------
# 2. Create backtest
# -----------------------------------------

from investos.portfolio.result import WeightsResult

# Add cash balance to starting weights, trades, and returns
df_weights_starting["cash"] = 1
df_trades["cash"] = 0
df_trades["cash"] -= df_trades.sum(axis=1)
df_returns["cash"] = 0

result = WeightsResult(
    initial_weights=df_weights_starting.iloc[0],
    trade_weights=df_trades,
    returns=df_returns,
    aum=50_000_000,
)

# -----------------------------------------
# 3. Save backtest
# -----------------------------------------

API_KEY = environ.get("ALVIN_OA_KEY")
API_ENDPOINT = "https://oa.app.forecastos.com/api/v1"

result.save(
    description="Showing Zhuo and Alvin ForecastOS",
    api_key=API_KEY,
    api_endpoint=API_ENDPOINT,
    team_ids=[4],
)
