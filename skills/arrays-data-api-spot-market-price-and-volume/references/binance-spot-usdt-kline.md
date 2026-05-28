# Binance spot USDT kline

`GET /api/v1/crypto/binance/spot/usdt/kline`

**Timestamp Rule**: query window is in UTC Unix seconds. Bar boundaries align to UTC (00:00 UTC for `1d`+). A bar is only returned if the query range fully contains `[time_open, time_close]`. The quote currency is fixed at USDT in the URL path — pass only the base token symbol (`BTC`, not `BTCUSDT`).

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Base token symbol, e.g. `BTC`, `ETH`, `SOL` |
| `start_time` | integer | yes | Start time (Unix seconds). Must be > 0 |
| `end_time` | integer | yes | End time (Unix seconds). Must be > start_time |
| `interval` | string | yes | `1min`, `2min`, `3min`, `5min`, `10min`, `15min`, `30min`, `45min`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1m`, `3m`, `6m` |
| `limit` | integer | no | Max data points. Default 500, max 10000 |

Response envelope: `{ "success": true, "data": [ ... ], "request_id": "..." }` — `data` is an array of candle items, in **reverse chronological order** (latest first).

**Each item in `data`:**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Time open | `time_open` | string | Bar open time, RFC 3339 (e.g. `"2025-11-05T00:00:00Z"`) |
| Time close | `time_close` | string | Bar close time, RFC 3339 |
| Open price | `price_open` | number | Opening price (USDT) |
| High price | `price_high` | number | Highest price in the interval (USDT) |
| Low price | `price_low` | number | Lowest price in the interval (USDT) |
| Close price | `price_close` | number | Closing price (USDT) |
| Volume | `volume` | number | Trading volume in **base-asset units** (BTC, ETH, etc.) — multiply by a representative bar price for USDT notional |
