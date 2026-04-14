# Market Metrics

`GET /api/v1/stocks/market-metrics`

Retrieve time series data for various market indicators, including technical and fundamental metrics.

**Indicator formats** — indicators requiring a period are formatted as `{INDICATOR}_{PERIOD}`:
- **PRICE_CHANGE**: `PRICE_CHANGE_1d`, `PRICE_CHANGE_1w`, `PRICE_CHANGE_1M`, `PRICE_CHANGE_3M`, `PRICE_CHANGE_6M`, `PRICE_CHANGE_ytd`, `PRICE_CHANGE_1y`, `PRICE_CHANGE_3y`, `PRICE_CHANGE_5y`
- **MA**: `MA_5`, `MA_10`, `MA_20`, `MA_60`, `MA_120`, `MA_200`
- **EMA**: `EMA_5`, `EMA_10`, `EMA_20`, `EMA_60`, `EMA_120`, `EMA_200`
- **VOLATILITY**: `VOLATILITY_20`, `VOLATILITY_60`, `VOLATILITY_90`
- **RSI**: `RSI_14`
- **MACD**: `MACD_12,26,9`
- **BOLLINGER**: `BOLLINGER_20,2`
- **VWAP**: `VWAP_DAY`
- **BETA**: `BETA` (default period `SPX_252`; interval must be `1d`)
- **AVERAGE_DAILY_DOLLAR_VOLUME**: `AVERAGE_DAILY_DOLLAR_VOLUME` (default period `20`; interval must be `1d`)
- **Fundamentals**: `MARKET_CAP`, `PE_RATIO`, `PS_RATIO`, `PB_RATIO`, `DIVIDEND_YIELD`, `ENTERPRISE_VALUE`, `EV_EBITDA_RATIO`

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interval` | string | yes | Time interval |
| `indicator` | string | yes | Indicator type (e.g., MA_20, PRICE_CHANGE_1d) |
| `symbol` | string | no | Stock symbol (optional, e.g., AAPL) |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |

**Response fields** (in `data` array — each element is a `MarketSymbolMetricData`):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol (e.g., AAPL) |
| `type` | string | Indicator type (e.g., MA_20) |
| `values` | array | Array of time series data points |

Each element in `values` (`MarketMetricValue`):

| Field | Type | Description |
|-------|------|-------------|
| `observed_at` | int64 | Observation timestamp (Unix seconds) |
| `date` | string | Formatted date (YYYY-MM-DD HH:mm:ss, UTC+0) |
| `value` | *float64 | Metric value (null if not available) |
| `metric_component` | string | Metric component label (e.g., UPPER); omitted when empty |

---
