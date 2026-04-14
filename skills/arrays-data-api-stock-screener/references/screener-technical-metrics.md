# Financial/technical metrics screener

`GET /api/v1/stocks/screener/technical-metrics`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `snapshot` | int | yes | Snapshot time (Unix seconds) |
| `metric_type` | string | yes | Metric type (see lists below) |
| `range_min` | float64 | no | Min value filter |
| `range_max` | float64 | no | Max value filter |
| `order_by` | string | no | `ASC` or `DESC` (default `DESC`) |

**Financial metric types**: `REVENUE_TTM`, `NET_INCOME_TTM`, `EPS_TTM`, `ROE_TTM`, `ROA_TTM`, `ROIC_TTM`, `GROSS_MARGIN_MRQ`, `OPERATING_MARGIN_MRQ`, `NET_MARGIN_MRQ`, `FCF_MARGIN_MRQ`, `CURRENT_RATIO_MRQ`, `DEBT_TO_EQUITY_MRQ`, `DEBT_TO_ASSETS_MRQ`, `NET_WORKING_CAPITAL_MRQ`, `QUICK_RATIO_MRQ`, `RD_TO_SALES_TTM`, `MARKET_CAP`, `PE_RATIO`, `PS_RATIO`, `PB_RATIO`, `DIVIDEND_YIELD`, `ENTERPRISE_VALUE`, `EV_EBITDA_RATIO`, and growth metrics (`REVENUE_GROWTH_QOQ`, `REVENUE_GROWTH_YOY_QUARTERLY`, `REVENUE_GROWTH_YOY_TTM`, `REVENUE_GROWTH_YOY_ANNUAL`, `EPS_GROWTH_QOQ`, `EPS_GROWTH_YOY_QUARTERLY`, `EPS_GROWTH_YOY_TTM`, `EPS_GROWTH_YOY_ANNUAL`, `FCF_GROWTH_QOQ`, `FCF_GROWTH_YOY_QUARTERLY`, `FCF_GROWTH_YOY_TTM`, `FCF_GROWTH_YOY_ANNUAL`)

**Technical metric types**: `PRICE_CHANGE_1D/1W/1M/3M/6M/YTD/1Y/3Y/5Y`, `SHARES_VOLUME`, `DOLLAR_VOLUME`, `AVERAGE_DAILY_DOLLAR_VOLUME`, `MA_5/10/20/60/120/200`, `EMA_5/10/20/60/120/200`, `RSI_14`, `MACD_DIF/DEA/HIST`, `BOLLINGER_UPPER/MID/LOWER`, `VWAP_DAY`, `BETA`, `VOLATILITY_20/60/90`

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `snapshot_time` | integer | Snapshot time as Unix timestamp in seconds (UTC) |
| `date` | string | Snapshot date in `YYYY-MM-DD` format |
| `metric` | string | Metric type that was queried (e.g. `PE_RATIO`, `MA_5`) |
| `value` | number | Metric value for this stock |
