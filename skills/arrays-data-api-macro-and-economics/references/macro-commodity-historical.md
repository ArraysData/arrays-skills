# 3. Historical data

`GET /api/v1/macro/commodity/historical`

These three endpoints share the same parameter and response structure (OHLCV daily bars).

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Symbol identifier. Index: e.g. `^GSPC`, `^DJI`, `^IXIC`. Forex: e.g. `EURUSD`, `GBPJPY`. Commodity: e.g. `GCUSD`, `HEUSX`, `SILUSD` |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `sort_order` | string | no | `desc` (default) = newest first; `asc` = oldest first (chronological). |

> **Sort order:** default is newest-first (`data[0]` = latest bar). Pass `sort_order=asc` for chronological order (oldest-first, so `data[-1]` = latest) — what SMA/ATR/rolling-window code expects.

> **Symbol:** exact and case-sensitive — `gcusd` and `GOLD` both return 400 (gold is `GCUSD`). Discover
> valid values with `GET /api/v1/macro/commodity/symbols`.

**Response** — `data` is an array of OHLCV bars, newest-first by default:
```json
{ "success": true, "request_id": "...", "data": [ { "symbol": "GCUSD", "date": "2025-08-18", "open": 2500.0, "close": 2510.0, ... } ] }
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Symbol identifier |
| `date` | string | Date (YYYY-MM-DD) |
| `open` | float | Opening price |
| `high` | float | Highest price |
| `low` | float | Lowest price |
| `close` | float | Closing price |
| `volume` | integer | Trading volume |
| `change` | float | Price change (may be omitted) |
| `change_percent` | float | Price change percentage (may be omitted) |
| `vwap` | float | Volume-weighted average price (may be omitted) |

**Python example:**
```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]
# Gold history, chronological order (sort_order=asc -> bars[-1] is the latest bar)
resp = requests.get(f"{base}/api/v1/macro/commodity/historical",
    params={"symbol": "GCUSD", "start_time": 1723939200, "end_time": 1726531200, "sort_order": "asc"},
    headers={"X-API-Key": key})
body = resp.json()
for bar in body["data"]:
    print(f"{bar['date']}: close={bar['close']}")
```

---
