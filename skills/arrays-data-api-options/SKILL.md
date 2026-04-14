---
name: arrays-data-api-options
description: Guides the agent to call Arrays REST APIs for stock options data — option contract specifications (strike, expiry, exercise style, active status) and options OHLCV/VWAP kline data. Use when the user asks about options pricing, strike prices, expiration dates, options volume, options VWAP, or historical options candlestick data.
---


# Arrays Data API — Options

Contract specifications and historical OHLCV/VWAP kline data for stock options.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- **OCC ticker format**: Options tickers follow the OCC format with `O:` prefix, e.g. `O:AAPL260410C00200000`. The format is `O:{SYMBOL}{YYMMDD}{C|P}{STRIKE*1000}`. Contracts endpoint returns tickers in the `options_ticker` field.
- **Real-time data workflow**: When a user asks for real-time or current options data by underlying symbol (e.g. "AAPL options"), the kline endpoint requires a specific `options_ticker`, not just the underlying symbol. You must do a **two-step lookup**:
  1. Call `/api/v1/options/contracts` with `symbol` to discover available contracts and their `options_ticker` values.
  2. Call `/api/v1/options/kline` with the specific `options_ticker` to get OHLCV/VWAP data.
- **Pagination**: `contracts` uses cursor-based pagination. Check `pagination.has_more`; if `true`, pass the `pagination.cursor` value as `cursor` in the next request.
- **Timestamps use Eastern Time**: Options endpoints use US Eastern Time. Always use `zoneinfo.ZoneInfo("America/New_York")` for timestamp computation, not UTC.
```python
from datetime import datetime
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York")
ts = int(datetime(2026, 4, 10, tzinfo=ET).timestamp())
```

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `options/contracts` | `contracts` | Option contract specifications and metadata |
| GET | `options/kline` | `kline` | Historical OHLCV and VWAP data for a specific option contract |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.

## Response format

**Contracts** uses a paginated wrapper:
```json
{
  "success": true,
  "data": [ ... ],
  "pagination": { "limit": 0, "cursor": "...", "has_more": true },
  "request_id": "..."
}
```

**Kline** returns a flat data array (no pagination):
```json
{
  "success": true,
  "data": [ ... ],
  "request_id": "..."
}
```

**Error**:
```json
{ "success": false, "data": null, "error": { "code": "VALIDATION_ERROR", "message": "..." }, "request_id": "..." }
```

Always check `success` before reading `data`.

## Python examples

```python
import requests, os
from datetime import datetime
from zoneinfo import ZoneInfo

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]
ET = ZoneInfo("America/New_York")

def to_ts(y, m, d):
    return int(datetime(y, m, d, tzinfo=ET).timestamp())

# Option contracts — list AAPL puts
resp = requests.get(f"{base}/api/v1/options/contracts",
    params={"symbol": "AAPL", "contract_type": "put", "limit": 5},
    headers={"X-API-Key": key})
body = resp.json()
if body.get("success") and body.get("data"):
    for c in body["data"]:
        print(f"{c['options_ticker']} strike={c['strike_price']} exp={c['expiration_date']} "
              f"style={c['exercise_style']}")

# Two-step workflow: underlying symbol → OHLCV/VWAP
# Step 1: Discover contracts
resp = requests.get(f"{base}/api/v1/options/contracts",
    params={"symbol": "AAPL", "contract_type": "call",
            "expiration_date_min": "2026-04-10", "limit": 5},
    headers={"X-API-Key": key})
body = resp.json()
if body.get("success") and body.get("data"):
    ticker = body["data"][0]["options_ticker"]  # e.g. "O:AAPL260410C00200000"

    # Step 2: Fetch kline for that contract
    resp = requests.get(f"{base}/api/v1/options/kline",
        params={"symbol": "AAPL", "options_ticker": ticker,
                "interval": "1d", "start_time": to_ts(2026, 4, 1),
                "end_time": to_ts(2026, 4, 10), "limit": 20},
        headers={"X-API-Key": key})
    kline = resp.json()
    if kline.get("success") and kline.get("data"):
        for bar in kline["data"]:
            print(f"Close: {bar['price_close']}, Vol: {bar['volume_traded']}, VWAP: {bar['vwap']}")
```
