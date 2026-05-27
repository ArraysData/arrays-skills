# Stock kline

`GET /api/v1/stocks/kline`

**Timestamp Rule**: US stock kline data is aligned to US Eastern time (ET), not UTC. A bar is only returned if the query range fully contains `[time_open, time_close]`.

**Bar boundaries by interval**:
- Intraday (`1min`–`4h`): RTH bars run 9:30–16:00 ET; ETH bars run 4:00–20:00 ET (pre-market through after-hours)
- `1d`: 9:30 ET – 16:00 ET (regular trading hours only; `session=ETH` not supported)
- `1w`: midnight ET Sunday – midnight ET next Sunday
- `1m`, `3m`, `6m`: midnight ET 1st of month/quarter – midnight ET 1st of next month/quarter

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (e.g. `AAPL`, `TSLA`) |
| `start_time` | integer | yes | Start time (Unix seconds). Must be > 0 |
| `end_time` | integer | yes | End time (Unix seconds). Must be > start_time |
| `interval` | string | yes | Time interval: `1min`, `2min`, `3min`, `5min`, `10min`, `15min`, `30min`, `45min`, `1h`, `2h`, `4h`, `1d`, `1w`, `1m`, `3m`, `6m` |
| `limit` | integer | no | Max data points. Default 100 |
| `session` | string | no | Trading session filter: `RTH` (9:30–16:00 ET) or `ETH` (default, includes pre/post market). Intraday intervals only — using `ETH` with `1d` or higher returns an error |

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of StockKlineData items.

**Each item in `data` (StockKlineData):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Time open | `time_open` | integer | K-line open time (Unix timestamp, seconds, UTC) |
| Time close | `time_close` | integer | K-line close time (Unix timestamp, seconds, UTC) |
| Period start | `time_period_start` | string | Open time in RFC 3339 format (e.g. `"2024-07-24T00:00:00Z"`) |
| Period end | `time_period_end` | string | Close time in RFC 3339 format |
| Open price | `price_open` | number | Opening price |
| Close price | `price_close` | number | Closing price |
| Low price | `price_low` | number | Lowest price |
| High price | `price_high` | number | Highest price |
| Trades count | `trades_count` | integer | Number of trades |
| Volume traded | `volume_traded` | number | Total traded volume |
