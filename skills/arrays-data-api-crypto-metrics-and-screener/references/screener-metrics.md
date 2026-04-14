# Crypto metrics screener

`GET /api/v1/crypto/screener/metrics`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `snapshot` | int | yes | Snapshot time (Unix seconds). Returns the most recent completed daily snapshot on or before this timestamp. To get data for a specific date, use end-of-day (`23:59:59 UTC`) or the next day's midnight (`00:00:00 UTC` of the following day). Using midnight of the target day returns the **previous** day's data. |
| `metric_type` | string | yes | See metric types below |
| `range_min` | float64 | no | Min value filter |
| `range_max` | float64 | no | Max value filter |
| `order_by` | string | no | `ASC` or `DESC` (default `DESC`) |

**Crypto metric types**: `MARKET_CAP`, `FDV`, `SHARES_VOLUME`, `PRICE_CHANGE_1D/1W/1M/3M/6M/YTD/1Y/3Y/5Y`, `MA_5/10/20/60/120/200`, `EMA_5/10/20/60/120/200`, `RSI_14`, `MACD_DIF/DEA/HIST`, `BOLLINGER_UPPER/MID/LOWER`, `BETA`, `VOLATILITY_20/60/90`

**Response fields** — V2 wrapper (`data` is an array):

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol (e.g. `"BTC"`) |
| `snapshot_time` | int64 | Snapshot time in Unix seconds |
| `date` | string | Date string (`YYYY-MM-DD`) |
| `metric` | string | Metric type identifier (e.g. `"MARKET_CAP"`) |
| `value` | float64 | Metric value |
