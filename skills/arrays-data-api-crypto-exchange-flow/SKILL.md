---
name: arrays-data-api-crypto-exchange-flow
description: Guides the agent to call Arrays REST APIs for crypto exchange flow data. Use when the user needs exchange inflow/outflow/netflow data for cryptocurrencies.
---


# Arrays Data API — Crypto Exchange Flow

**Domain**: `crypto_exchange_flow`. Exchange inflow, outflow, and net flow data for crypto tokens.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- **Data ordering**: Results are returned in **reverse chronological order** (latest first). When querying for data "on" a specific date (e.g., `start_time=Oct20, end_time=Oct21`), `data[0]` is the NEXT day's data and `data[-1]` is the target day's data. **Always match by the `date` field** or use `data[-1]` to get the target date.
- **Timestamp computation**: Always use Python `datetime` + `calendar` to compute Unix timestamps. Do NOT calculate timestamps by mental arithmetic.
```python
import calendar
from datetime import datetime, timezone
ts = int(calendar.timegm(datetime(2025, 8, 13, 0, 0, 0, tzinfo=timezone.utc).timetuple()))
```

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `exchange-flows` | `exchange-flows` | Exchange flows |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Response format

The response uses V2 format with a **flat `data` array** (not nested):

```json
{
  "success": true,
  "data": [
    {
      "symbol": "BTC",
      "exchange": "binance",
      "datetime": 1723507200,
      "date": "2025-08-13",
      "window": "day",
      "netflow_total": 3114.45,
      "inflow_total": 15678.90,
      "outflow_total": 12564.45,
      "inflow_top10": 5000.00,
      "inflow_mean": 156.78,
      "inflow_mean_ma7": 160.12,
      "outflow_top10": 4000.00,
      "outflow_mean": 125.64,
      "outflow_mean_ma7": 130.00
    }
  ]
}
```

**Response fields** (in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Symbol, e.g., BTC, ETH |
| `exchange` | string | Exchange name, e.g., binance |
| `datetime` | int64 | Unix timestamp (seconds) |
| `date` | string | Formatted date (YYYY-MM-DD, UTC+0) |
| `window` | string | Time window granularity: hour/day |
| `netflow_total` | float64 | Net flow = inflow_total - outflow_total |
| `inflow_total` | float64 | Total inflow |
| `inflow_top10` | float64 | Top10 address inflow |
| `inflow_mean` | float64 | Average inflow |
| `inflow_mean_ma7` | float64 | 7-period moving average inflow |
| `outflow_total` | float64 | Total outflow |
| `outflow_top10` | float64 | Top10 address outflow |
| `outflow_mean` | float64 | Average outflow |
| `outflow_mean_ma7` | float64 | 7-period moving average outflow |

## Python example

```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# Get BTC daily exchange flow for a specific date
# Data is reverse chronological — match by date field, NOT data[0]
import calendar
from datetime import datetime, timezone
def to_ts(y, m, d, h=0):
    return int(calendar.timegm(datetime(y, m, d, h, tzinfo=timezone.utc).timetuple()))

resp = requests.get(f"{base}/api/v1/crypto/exchange-flows",
    params={"symbol": "BTC", "start_time": to_ts(2025, 8, 13),
            "end_time": to_ts(2025, 8, 14), "window": "day", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    flows = body["data"]  # flat array, reverse chronological
    # Match by target date (NOT data[0] which may be next day)
    for f in flows:
        if f["date"] == "2025-08-13":
            print(f"Netflow: {f['netflow_total']}")
            break
```
