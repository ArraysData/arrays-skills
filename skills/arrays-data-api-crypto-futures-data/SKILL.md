---
name: arrays-data-api-crypto-futures-data
description: Calls Arrays REST APIs for crypto derivatives data — funding rates, open interest, long-short ratios, and taker buy/sell volume. Use when the user asks about perpetual futures, funding costs, leveraged positions, derivatives market sentiment, or futures data for any cryptocurrency.
---

# Arrays Data API — Crypto Futures Data

Funding rate, open interest, long-short ratio, and taker buy/sell volume for crypto futures.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Endpoints

All under prefix `/api/v1/tokens/`:

| Method | Path | Description |
|--------|------|-------------|
| GET | `funding-rate` | Futures funding rate |
| GET | `open-interest` | Open interest data |
| GET | `long-short-ratio` | Long/short ratio |
| GET | `taker-buy-sell-volume` | Taker buy/sell volume ratio |

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

## Per-endpoint response details

### GET `funding-rate`

Binance funding rates settle every **8 hours** at 00:00, 08:00, 16:00 UTC. Query for exact settlement times only.

**CRITICAL — Fallback for missing settlement times**: Some tokens only have data at certain settlement times (e.g., AAVE only has 00:00 UTC). If querying a specific settlement time returns **empty `data`**, you MUST immediately retry with a full-day range (`start_time=day_start, end_time=next_day_start`) and report any available funding rate for that day. Never output "No data" or "API_ERROR" without trying the full-day fallback first. Filter the results to match the target date's timestamp.

```python
from datetime import timedelta

# Fallback pattern for funding rate queries:
resp = requests.get(f"{base}/api/v1/tokens/funding-rate",
    params={"symbol": symbol, "start_time": target_ts, "end_time": target_ts + 3600},
    headers={"X-API-Key": key})
data = resp.json().get("data", [])
if not data:  # No data at requested time — fallback to full day
    day_start = to_ts(year, month, day, 0)
    # IMPORTANT: use timedelta to safely get next day (handles month boundaries like Nov 30 → Dec 1)
    next_day = datetime(year, month, day, tzinfo=timezone.utc) + timedelta(days=1)
    day_end = int(calendar.timegm(next_day.timetuple()))
    resp = requests.get(f"{base}/api/v1/tokens/funding-rate",
        params={"symbol": symbol, "start_time": day_start, "end_time": day_end},
        headers={"X-API-Key": key})
    data = resp.json().get("data", [])
    # Filter for target date
    data = [d for d in data if d["time"].startswith(f"{year}-{month:02d}-{day:02d}")]
if data:
    print(data[0]["fundingRate"])
```

```json
{
  "success": true,
  "data": [
    { "symbol": "BTCUSDT", "fundingRate": 0.0001, "timestamp": 1723507200, "time": "2025-08-13T00:00:00Z" }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Trading pair symbol |
| `fundingRate` | float64 | Funding rate value. Positive means longs pay shorts; negative means shorts pay longs. |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | ISO 8601 / RFC 3339 time string (e.g. `2025-08-13T00:00:00Z`) |

---

### GET `open-interest`

```json
{
  "success": true,
  "data": [
    { "symbol": "ETHUSDT", "sumOpenInterestValue": 10838759439, "timestamp": 1723507200, "time": "2025-08-14T00:00:00Z" }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Trading pair symbol |
| `sumOpenInterestValue` | float64 | Total open interest value in USD |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | ISO 8601 / RFC 3339 time string |

---

### GET `long-short-ratio`

```json
{
  "success": true,
  "data": [
    { "symbol": "BTCUSDT", "longShortRatio": 1.61, "timestamp": 1723507200, "time": "2025-08-13T00:00:00Z" }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Trading pair symbol |
| `longShortRatio` | float64 | Long/short ratio. >1.0 means more long; <1.0 means more short. |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | ISO 8601 / RFC 3339 time string |

---

### GET `taker-buy-sell-volume`

**CRITICAL**: `buyVol` and `sellVol` are in **base asset quantity** (e.g., ETH for ETHUSDT), NOT USD. To get USD volume, multiply by the token price from the `tokens/kline` endpoint.

**WARNING — DO NOT use this endpoint for "futures trading volume" queries.** This endpoint only provides taker buy/sell breakdown (in base asset, not USD). For total futures trading volume, you MUST use the `tokens/futures/ohlcv-full-bar-data` endpoint instead — it returns `volume_traded` directly in **quote currency (USDT)** with no conversion needed. Call it like this:
```python
resp = requests.get(f"{base}/api/v1/tokens/futures/ohlcv-full-bar-data",
    params={"symbol": "ETHUSDT", "start_time": start, "end_time": end, "interval": "1d", "limit": 5},
    headers={"X-API-Key": key})
body = resp.json()
# Data is reverse chronological — use data[-1] for the target date
target = [d for d in body["data"] if d["time_period_start"].startswith("2025-09-06")]
volume_usd = target[0]["volume_traded"] if target else body["data"][-1]["volume_traded"]
```

```json
{
  "success": true,
  "data": [
    { "buyVol": 19037814781.55, "sellVol": 18442110914.54, "buySellRatio": 1.032, "timestamp": 1723507200 }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `buyVol` | float64 | Taker buy volume in **base asset quantity** (e.g. ETH for ETHUSDT). Multiply by price to get USD. |
| `sellVol` | float64 | Taker sell volume in **base asset quantity**. Multiply by price to get USD. |
| `buySellRatio` | float64 | Buy/sell volume ratio. >1.0 means more buying pressure. |
| `timestamp` | int64 | Unix timestamp in seconds |

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
resp = requests.get(f"{base}/api/v1/tokens/funding-rate",
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
    resp = requests.get(f"{base}/api/v1/tokens/funding-rate",
        params={"symbol": "ETHUSDT", "start_time": day_start, "end_time": day_end,
                "limit": 10, "exchange": "binance"},
        headers={"X-API-Key": key})
    data = resp.json().get("data", [])
    data = [d for d in data if d["time"].startswith(f"{year}-{month:02d}-{day:02d}")]
for item in data:
    print(f"Time: {item['time']}, Funding Rate: {item['fundingRate']}")

# Get taker buy/sell volume and convert to USD
start = to_ts(2025, 9, 6)
end = to_ts(2025, 9, 7)
# Step 1: get volume (in base asset, e.g. ETH)
resp = requests.get(f"{base}/api/v1/tokens/taker-buy-sell-volume",
    params={"symbol": "ETHUSDT", "start_time": start, "end_time": end,
            "interval": "1d", "exchange": "binance"},
    headers={"X-API-Key": key})
vol = resp.json()["data"][0]
# Step 2: get price to convert to USD
resp2 = requests.get(f"{base}/api/v1/tokens/kline",
    params={"symbol": "ETH", "start_time": start, "end_time": end,
            "interval": "1d", "limit": 1},
    headers={"X-API-Key": key})
price = resp2.json()["response"]["data"][0]["price_close"]
total_vol_usd = (vol["buyVol"] + vol["sellVol"]) * price
print(f"${total_vol_usd:,.2f}")

# Get open interest for a specific day
start = to_ts(2025, 11, 11)
end = to_ts(2025, 11, 12)
resp = requests.get(f"{base}/api/v1/tokens/open-interest",
    params={"symbol": "ETHUSDT", "start_time": start, "end_time": end,
            "interval": "1d", "exchange": "binance"},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    for item in body["data"]:
        print(f"Open Interest: ${item['sumOpenInterestValue']:,.2f}")
```
