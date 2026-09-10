# 3. Historical data

`GET /api/v1/macro/index/historical`

These three endpoints share the same parameter and response structure (OHLCV daily bars).

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Symbol identifier. Index: e.g. `^SPX`, `^DJI`, `^IXIC`. Forex: e.g. `EURUSD`, `GBPJPY`. Commodity: e.g. `GCUSD`, `HEUSX`, `SILUSD` |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `sort_order` | string | no | `desc` (default) = newest first; `asc` = oldest first (chronological). |

> **Sort order:** default is newest-first (`data[0]` = latest bar). Pass `sort_order=asc` for chronological order (oldest-first, so `data[-1]` = latest) — what SMA/ATR/rolling-window code expects.

> **Symbol:** case-insensitive and the `^` is optional (`spx` = `^SPX`). Aliases resolve as listed below;
> anything else must be a canonical symbol from `GET /api/v1/macro/index/symbols`
> (`macro-index-symbol-list.md`).

**Common indexes and aliases**

| Index | Alias | Resolves to |
|-------|-------|-------------|
| S&P 500 | `GSPC`, `SP500`, `SPX500`, `US500` | `^SPX` |
| Dow Jones Industrial Average | — | `^DJI` |
| NASDAQ Composite | — | `^IXIC` |
| NASDAQ 100 | `NASDAQ100`, `NDX100` | `^NDX` |
| Russell 2000 | — | `^RUT` |
| CBOE Volatility Index | — | `^VIX` |
| US Dollar Index | `DXY`, `USDX`, `USDOLLAR` | `DX-Y.NYB` |
| Nikkei 225 | `NIKKEI` | `^N225` |
| Treasury yield, 10 years | `10Y`, `US10Y` | `^TNX` |
| Treasury yield, 30 years | `30Y` | `^TYX` |
| Treasury yield, 5 years | `5Y` | `^FVX` |
| Treasury bill, 13 weeks | `3M` | `^IRX` |

**Response** — `data` is an array of OHLCV bars, newest-first by default:
```json
{ "success": true, "request_id": "...", "data": [ { "symbol": "^SPX", "date": "2025-08-18", "open": 5600.0, "close": 5620.0, ... } ] }
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Canonical index symbol — may differ from what you sent (`DXY` → `DX-Y.NYB`) |
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
# S&P 500 history, chronological order (sort_order=asc -> bars[-1] is the latest bar)
resp = requests.get(f"{base}/api/v1/macro/index/historical",
    params={"symbol": "^SPX", "start_time": 1723939200, "end_time": 1726531200, "sort_order": "asc"},
    headers={"X-API-Key": key})
body = resp.json()
for bar in body["data"]:
    print(f"{bar['date']}: close={bar['close']}")
```

---
