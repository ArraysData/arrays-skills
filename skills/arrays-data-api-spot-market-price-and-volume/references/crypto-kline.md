# Crypto kline

`GET crypto/kline`

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of KlineData items.

**Each item in `data` (KlineData):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Time open | `time_open` | integer | K-line open time (Unix timestamp, seconds, UTC) |
| Time close | `time_close` | integer | K-line close time (Unix timestamp, seconds, UTC) |
| Period start | `time_period_start` | string | Open time in RFC 3339 format (e.g. `"2024-07-24T00:00:00Z"`) |
| Period end | `time_period_end` | string | Close time in RFC 3339 format |
| Open price | `price_open` | number | Opening price |
| Close price | `price_close` | number | Closing price |
| Low price | `price_low` | number | Lowest price in the interval |
| High price | `price_high` | number | Highest price in the interval |
| Trades count | `trades_count` | integer | Number of trades in the interval |
| Volume traded | `volume_traded` | number | Quote-currency trading volume |
