---
name: arrays-data-api-crypto-exchange-flow
description: Guides the agent to call Arrays REST APIs for crypto exchange flow data. Use when the user needs exchange inflow/outflow/netflow data for cryptocurrencies.
---

# Arrays Data API — Crypto Exchange Flow

**Domain**: `crypto_exchange_flow`. Exchange inflow, outflow, and net flow data for crypto tokens.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Endpoints

- **Prefix**: `/api/v1/tokens/`
- **Path** (GET): `exchange-flows` — crypto exchange flow data (inflow/outflow/netflow)

## Important notes

- **Data ordering**: Results are returned in **reverse chronological order** (latest first). When querying for data "on" a specific date (e.g., `start_time=Oct20, end_time=Oct21`), `data[0]` is the NEXT day's data and `data[-1]` is the target day's data. **Always match by the `date` field** or use `data[-1]` to get the target date.
- **Timestamp computation**: Always use Python `datetime` + `calendar` to compute Unix timestamps. Do NOT calculate timestamps by mental arithmetic.
```python
import calendar
from datetime import datetime, timezone
ts = int(calendar.timegm(datetime(2025, 8, 13, 0, 0, 0, tzinfo=timezone.utc).timetuple()))
```

## Parameters

### Exchange flows (`exchange-flows`)

Get crypto exchange inflow/outflow data for BTC and ETH from Binance. Symbol parameter is case-insensitive.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (case-insensitive, e.g., BTC, btc, ETH, eth) |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `limit` | integer | no | Maximum number of records (default: 50, max: 1000) |
| `window` | string | no | Time window granularity: `hour` or `day`. Default: `hour` |

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
      "netflowTotal": 3114.45,
      "inflowTotal": 15678.90,
      "outflowTotal": 12564.45,
      "inflowTop10": 5000.00,
      "inflowMean": 156.78,
      "inflowMeanMa7": 160.12,
      "outflowTop10": 4000.00,
      "outflowMean": 125.64,
      "outflowMeanMa7": 130.00
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
| `netflowTotal` | float64 | Net flow = inflowTotal - outflowTotal |
| `inflowTotal` | float64 | Total inflow |
| `inflowTop10` | float64 | Top10 address inflow |
| `inflowMean` | float64 | Average inflow |
| `inflowMeanMa7` | float64 | 7-period moving average inflow |
| `outflowTotal` | float64 | Total outflow |
| `outflowTop10` | float64 | Top10 address outflow |
| `outflowMean` | float64 | Average outflow |
| `outflowMeanMa7` | float64 | 7-period moving average outflow |

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

resp = requests.get(f"{base}/api/v1/tokens/exchange-flows",
    params={"symbol": "BTC", "start_time": to_ts(2025, 8, 13),
            "end_time": to_ts(2025, 8, 14), "window": "day", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    flows = body["data"]  # flat array, reverse chronological
    # Match by target date (NOT data[0] which may be next day)
    for f in flows:
        if f["date"] == "2025-08-13":
            print(f"Netflow: {f['netflowTotal']}")
            break
```
