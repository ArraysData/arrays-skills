# 3. Historical data

`GET /api/v1/macro/commodity/historical`

These three endpoints share the same parameter and response structure (OHLCV daily bars).

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Symbol identifier. Index: e.g. `^GSPC`, `^DJI`, `^IXIC`. Forex: e.g. `EURUSD`, `GBPJPY`. Commodity: e.g. `GCUSD`, `HEUSX`, `SILUSD` |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |

**Response** — `data` is an array of OHLCV bars:
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
# Get gold historical data
resp = requests.get(f"{base}/api/v1/macro/commodity/historical",
    params={"symbol": "GCUSD", "start_time": 1723939200, "end_time": 1723939200},
    headers={"X-API-Key": key})
body = resp.json()
bars = body["data"]  # array of OHLCV bars
for bar in bars:
    print(f"{bar['date']}: close={bar['close']}")
```

---
