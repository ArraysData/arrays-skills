---
name: arrays-data-api-crypto-futures-data
description: Calls Arrays REST APIs for crypto derivatives data — funding rates, open interest, long-short ratios, and taker buy/sell volume. Use when the user asks about perpetual futures, funding costs, leveraged positions, derivatives market sentiment, or futures data for any cryptocurrency.
---


# Arrays Data API — Crypto Futures Data

Funding rate, open interest, long-short ratio, and taker buy/sell volume for crypto futures.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- **Data ordering**: Results are returned in **reverse chronological order** (latest first). When querying for data "on" a specific date, the query `start_time=target_day, end_time=next_day` returns two data points: `data[0]` is the next day's value (NOT the target) and `data[-1]` is the target day's value. **Always match by timestamp or use `data[-1]`** to get the target date's data point.
- **Funding rate settlement**: Binance funding rates settle every 8 hours at **00:00, 08:00, 16:00 UTC**. Only query for exact settlement times. When querying a specific settlement, set `start_time` to the exact settlement time and **`end_time` to `start_time + 3600`** (1 hour after). NEVER use `end_time = start_time + 1` — a window of just 1 second will return NO results. Always add at least 3600 seconds.
- **Timestamp computation**: Always use Python `datetime` + `calendar` + `timedelta` to compute Unix timestamps. Do NOT calculate timestamps by mental arithmetic — this is error-prone. Always use `timedelta(days=1)` to compute "next day" — never `day + 1` (which crashes on month boundaries like Nov 30 → "Nov 31").

```python
import calendar
from datetime import datetime, timezone, timedelta
# Example: November 30, 2025 00:00:00 UTC
target = datetime(2025, 11, 30, 0, 0, 0, tzinfo=timezone.utc)
ts = int(calendar.timegm(target.timetuple()))
# Safe next-day calculation (Nov 30 → Dec 1):
next_day_ts = int(calendar.timegm((target + timedelta(days=1)).timetuple()))
```

## Common parameters

All four endpoints share the same parameter set:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Trading pair symbol (e.g. `BTCUSDT`, `ETHUSDT`). Use the concatenated format, not just the base symbol. |
| `start_time` | int64 | yes | Start timestamp (Unix seconds) |
| `end_time` | int64 | yes | End timestamp (Unix seconds) |
| `limit` | int32 | no | Max results (1-1000, default 30) |
| `interval` | string | no | Time interval (only `1d` supported, default `1d`). Not applicable to `funding-rate`. |
| `exchange` | string | no | Exchange name (only `binance` supported, default `binance`) |

## Response format

All endpoints return V2 format with a **flat `data` array**:

```json
{ "success": true, "data": [ ... ] }
```

Always check `body["success"]` before reading `body["data"]`.

**Error**:
```json
{ "success": false, "error": { "code": "INVALID_TIMESTAMP", "message": "..." } }
```

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `funding-rate` | `funding-rate` | Funding Rate |
| GET | `open-interest` | `open-interest` | Open Interest |
| GET | `long-short-ratio` | `long-short-ratio` | Long Short Ratio |
| GET | `taker-buy-sell-volume` | `taker-buy-sell-volume` | Taker Buy Sell Volume |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Python example

```python
import requests, os, calendar
from datetime import datetime, timezone, timedelta

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# ALWAYS use datetime to compute timestamps — never mental arithmetic
def to_ts(year, month, day, hour=0):
    return int(calendar.timegm(datetime(year, month, day, hour, tzinfo=timezone.utc).timetuple()))

# Get funding rate with fallback for missing settlement times
# IMPORTANT: end_time must be start_time + 3600 (NOT +1, which returns nothing)
target_hour = 16  # e.g., 16:00 UTC settlement
year, month, day = 2025, 8, 14
start = to_ts(year, month, day, target_hour)
end = start + 3600
resp = requests.get(f"{base}/api/v1/crypto/funding-rate",
    params={"symbol": "ETHUSDT", "start_time": start, "end_time": end,
            "limit": 10, "exchange": "binance"},
    headers={"X-API-Key": key})
body = resp.json()
data = body.get("data", [])
if not data:  # Fallback: query full day if specific time has no data
    day_start = to_ts(year, month, day, 0)
    # Use timedelta for safe next-day calculation (handles month boundaries like Nov 30 → Dec 1)
    next_day = datetime(year, month, day, tzinfo=timezone.utc) + timedelta(days=1)
    day_end = int(calendar.timegm(next_day.timetuple()))
    resp = requests.get(f"{base}/api/v1/crypto/funding-rate",
        params={"symbol": "ETHUSDT", "start_time": day_start, "end_time": day_end,
                "limit": 10, "exchange": "binance"},
        headers={"X-API-Key": key})
    data = resp.json().get("data", [])
    data = [d for d in data if d["time"].startswith(f"{year}-{month:02d}-{day:02d}")]
for item in data:
    print(f"Time: {item['time']}, Funding Rate: {item['funding_rate']}")

# Get taker buy/sell volume and convert to USD
start = to_ts(2025, 9, 6)
end = to_ts(2025, 9, 7)
# Step 1: get volume (in base asset, e.g. ETH)
resp = requests.get(f"{base}/api/v1/crypto/taker-buy-sell-volume",
    params={"symbol": "ETHUSDT", "start_time": start, "end_time": end,
            "interval": "1d", "exchange": "binance"},
    headers={"X-API-Key": key})
vol = resp.json()["data"][0]
# Step 2: get price to convert to USD
resp2 = requests.get(f"{base}/api/v1/crypto/kline",
    params={"symbol": "ETH", "start_time": start, "end_time": end,
            "interval": "1d", "limit": 1},
    headers={"X-API-Key": key})
price = resp2.json()["data"][0]["price_close"]
total_vol_usd = (vol["buy_vol"] + vol["sell_vol"]) * price
print(f"${total_vol_usd:,.2f}")

# Get open interest for a specific day
start = to_ts(2025, 11, 11)
end = to_ts(2025, 11, 12)
resp = requests.get(f"{base}/api/v1/crypto/open-interest",
    params={"symbol": "ETHUSDT", "start_time": start, "end_time": end,
            "interval": "1d", "exchange": "binance"},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    for item in body["data"]:
        print(f"Open Interest: ${item['sum_open_interest_value']:,.2f}")
```
