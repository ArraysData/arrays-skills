# Market metrics

`GET /api/v1/crypto/market-metrics`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interval` | string | yes | Time interval: `1d`, `1w`, `1m` |
| `indicator` | string | yes | Indicator type (e.g. `MA_20`, `PRICE_CHANGE_1d`, `MARKET_CAP`, `FDV`) |
| `symbol` | string | no | Token symbol (e.g. `BTCUSDT`); returns all if omitted |
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds) |

**Response fields** — V2 wrapper (`data` is an array of per-symbol objects):

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol (e.g. `"BTCUSDT"`) |
| `type` | string | Indicator type (e.g. `"MA_20"`) |
| `values` | array | Array of time-series data points |

Each item in `values`:

| Field | Type | Description |
|-------|------|-------------|
| `observed_at` | int64 | Unix timestamp in seconds |
| `date` | string | Formatted date (`YYYY-MM-DD HH:mm:ss`, UTC+0) |
| `value` | float64 or null | Metric value (null if not available) |
| `metric_component` | string | Sub-component label (e.g. `"UPPER"`, `"MID"`, `"LOWER"` for Bollinger; `"DIF"`, `"DEA"`, `"HIST"` for MACD). Omitted for single-value indicators |
