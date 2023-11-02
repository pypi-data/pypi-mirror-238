import pandas as pd
import numpy as np
from os import environ

# -----------------------------------------
# 1. Read and transform data
# -----------------------------------------

# Read data
active_positions_filename = "/Users/johnreese/Downloads/delphia-am-prod_DCMF-august-release-2023-07-25-v013-monthly_daily_positions_output_active_portfolio_full_daily_positions.parquet"
active_returns_filename = "/Users/johnreese/Downloads/delphia-am-prod_DCMF-august-release-2023-07-25-v013-monthly_daily_positions_input_daily_returns.parquet"
active_attributed_returns_filename = "/Users/johnreese/Downloads/delphia-am-prod_DCMF-august-release-2023-07-25-v013-monthly_reports_output_active_portfolio_attributed_returns.parquet"

df_weights_starting = pd.read_parquet(active_positions_filename)
df_returns = pd.read_parquet(active_returns_filename)
df_attr_returns = pd.read_parquet(active_attributed_returns_filename)

# Pivot holdings into expected format
df_weights_starting = (
    df_weights_starting["initial_weights"]
    .reset_index()
    .pivot(index="date", columns="company_id", values="initial_weights")
    .fillna(0)
)

# Calculate ending weights
df_weights_ending = df_weights_starting.shift(-1)

# Calculate trades (WHICH SEEM TO HAPPEN AFTER ATTR RETURNS)
df_returns_pivoted = (
    df_returns.reset_index()
    .pivot(index="date", columns="company_id", values="returns")
    .fillna(0)
)

# Calculate trades (WHICH SEEM TO HAPPEN AFTER ATTR RETURNS)
df_attr_returns_pivoted = (
    df_attr_returns.reset_index()
    .pivot(index="date", columns="company_id", values="returns")
    .fillna(0)
)

# Keep only dates in weights starting
df_returns_pivoted = df_returns_pivoted[
    df_returns_pivoted.index.isin(df_weights_starting.index)
]

s_scaling_factor = (1 + df_attr_returns_pivoted.sum(axis=1)).cumprod()
s_scaling_factor.iloc[0] = 1

# Scale starting and ending weights
df_weights_ending = df_weights_ending.multiply(s_scaling_factor, axis=0)
df_weights_starting = df_weights_starting.multiply(
    s_scaling_factor.shift(1).fillna(method="bfill"), axis=0
)

# Scale attr returns
df_attr_returns_pivoted = df_attr_returns_pivoted.multiply(s_scaling_factor, axis=0)

# Start weights at 0 for T=0 (before AUM is invested)
new_row = pd.DataFrame(
    [], index=[df_attr_returns_pivoted.index[0] - pd.Timedelta(days=1)]
)

df_returns_pivoted = pd.concat([new_row, df_returns_pivoted]).fillna(0)
df_attr_returns_pivoted = pd.concat([new_row, df_attr_returns_pivoted]).fillna(0)
df_weights_starting = pd.concat([new_row, df_weights_starting]).fillna(0)
df_weights_ending = pd.concat([new_row, df_weights_ending]).fillna(0)
df_weights_ending.iloc[0] = df_weights_starting.iloc[1]

# Trades
# df_trades = (df_weights_ending - df_attr_returns_pivoted - df_weights_starting).fillna(
#     0
# )
df_trades = (
    df_weights_ending - df_returns_pivoted * df_weights_starting - df_weights_starting
).fillna(0)

# Calculate returns by company (note: trades happen after attr returns)
df_returns = df_returns_pivoted.fillna(0).replace([np.inf, -np.inf], 0)

# -----------------------------------------
# 2. Create backtest
# -----------------------------------------
import investos as inv
from investos.portfolio.result import WeightsResult

inv.api_endpoint = "http://localhost:3000/api/v1"
# inv.api_endpoint = "https://oa.app.forecastos.com/api/v1"
# inv.api_key = environ.get("ALVIN_OA_KEY")

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

result.summary

# -----------------------------------------
# 3. Save backtest
# -----------------------------------------

result.save(
    description="Running backtest for Dan",
)
result.save_chart_hit_rate(df_returns)
