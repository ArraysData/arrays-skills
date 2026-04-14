# Darkpool

`GET /api/v1/stocks/darkpool`

Retrieve darkpool trading data for specified stock symbols within a time range. Returns hourly aggregated OHLC and volume data.

**IMPORTANT**: Data is aggregated hourly. The `timestamp` field represents the **start** of each hour in UTC. When looking for data at a specific hour (e.g., 18:00 UTC), compute the target hour-start timestamp using `datetime` and compare with equality. For example, 2025-12-04 18:00 UTC → `int(calendar.timegm(datetime(2025, 12, 4, 18, tzinfo=timezone.utc).timetuple()))`.

**IMPORTANT**: To get data for a full day including evening hours, set `end_time` to the **next day's** timestamp. For example, to get all Dec 4 data, use `start_time` for 2025-12-04 00:00 UTC and `end_time` for 2025-12-05 00:00 UTC.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (e.g., AAPL) |
| `start_time` | int64 | yes | Start time (Unix timestamp in seconds) |
| `end_time` | int64 | yes | End time (Unix timestamp in seconds) |

**Response fields** (in `data` array — each element is a `DarkpoolOHLCData`):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `timestamp` | int64 | Hourly timestamp (Unix seconds, UTC) — start of the hour |
| `open` | string | Opening price in the hour |
| `high` | string | Highest price in the hour |
| `low` | string | Lowest price in the hour |
| `close` | string | Closing price in the hour |
| `volume` | int64 | Total trading volume |
| `trade_count` | int32 | Number of trades executed |
| `total_value` | string | Total transaction value |
| `vwap` | string | Volume Weighted Average Price |

---
