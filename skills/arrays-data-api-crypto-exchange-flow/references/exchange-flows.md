# Exchange flows

`GET /api/v1/crypto/exchange-flows`

Get crypto exchange inflow/outflow data for BTC and ETH from Binance. Symbol parameter is case-insensitive.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (case-insensitive, e.g., BTC, btc, ETH, eth) |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `limit` | integer | no | Maximum number of records (default: 50, max: 1000) |
| `window` | string | no | Time window granularity: `hour` or `day`. Default: `hour` |

**Response fields** (each item in `data` array)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `exchange` | string | Exchange (e.g., `binance`) |
| `date` | string | Date (`YYYY-MM-DD`) |
| `datetime` | int64 | Unix timestamp in seconds |
| `window` | string | Time window granularity (`hour` or `day`) |
| `inflow_total` | float64 | Total inflow |
| `inflow_top10` | float64 | Top-10 address inflow |
| `inflow_mean` | float64 | Mean inflow |
| `inflow_mean_ma7` | float64 | 7-period moving average of mean inflow |
| `outflow_total` | float64 | Total outflow |
| `outflow_top10` | float64 | Top-10 address outflow |
| `outflow_mean` | float64 | Mean outflow |
| `outflow_mean_ma7` | float64 | 7-period moving average of mean outflow |
| `netflow_total` | float64 | Net flow (inflow − outflow) |
