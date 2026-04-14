# Stock kline

`GET stocks/kline`

**Timestamp Rule**: US stock kline data is aligned to US Eastern time (ET), not UTC. To include a full day's data, set `end_time` to midnight ET of the **next** day — e.g. for 2024-12-31: `end_time = int(datetime(2025, 1, 1, 0, 0, 0, tzinfo=ET).timestamp())`. Using tight UTC-based ranges will miss candles.

**Weekly candles**: Weekly candles start on **Sunday** ET (not Monday). For "week of Jan 6 (Monday)", the candle starts on Jan 5 (Sunday). Use `start_time = Jan 5` to get that week's data.

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
