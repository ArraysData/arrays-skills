---
name: arrays-data-api-options
description: Guides the agent to call Arrays REST APIs for stock options data — option contract specifications (strike, expiry, exercise style, active status), options OHLCV/VWAP kline data, historical option Greeks (delta, gamma, theta, vega) with implied volatility, and full option-chain snapshots (every contract on an underlying with OHLCV, Greeks, IV, open interest). Use when the user asks about options pricing, strike prices, expiration dates, options volume, options VWAP, options candlestick data, option Greeks, delta/gamma/theta/vega, implied volatility, open interest, or an option chain for a ticker.
---


# Arrays Data API — Options

Contract specifications, OHLCV/VWAP kline data, historical Greeks, and full chain snapshots for stock options. See the endpoint table below for what each one covers.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- **OCC ticker format**: Options tickers follow the OCC format `{SYMBOL}{YYMMDD}{C|P}{STRIKE*1000}`, usually with an `O:` prefix, e.g. `O:AAPL260410C00200000`. The contracts endpoint returns them in the `options_ticker` field. **Exception**: the `chain` endpoint's `option_ticker` param takes the **bare OCC ticker** with **no** `O:` prefix (e.g. `AAPL260612C00120000`).
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

- **Prefix**: `/api/v1/options/`

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `contracts` | `contracts` | Specs/metadata for an underlying's whole option chain (active or expired), filterable by expiration, strike, and type |
| GET | `kline` | `kline` | Historical and real-time OHLCV/VWAP for a single contract |
| GET | `greeks` | `greeks` | Daily in-house Greeks (delta, gamma, theta, vega) and IV for a single contract |
| GET | `chain` | `chain` | Previous-day snapshot of an underlying's whole chain (OHLCV, Greeks, IV, open interest) |

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

**Chain** is also paginated, but its contracts are nested one level deeper — the single `data[0].results` array holds the contracts:
```json
{
  "success": true,
  "data": [ { "results": [ ... ], "cursor": "..." } ],
  "pagination": { "limit": 0, "cursor": "...", "has_more": true },
  "request_id": "..."
}
```

**Kline** and **greeks** return a flat data array (no pagination):
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

# Historical Greeks for a specific contract (uses options_ticker + date range)
resp = requests.get(f"{base}/api/v1/options/greeks",
    params={"options_ticker": "O:SPY260501C00500000",
            "start_date": "2026-04-01", "end_date": "2026-05-01"},
    headers={"X-API-Key": key})
body = resp.json()
if body.get("success") and body.get("data"):
    for row in body["data"]:
        # delta/gamma/theta/vega and implied_volatility are null when status is iv_failed/pricing_failed
        if row.get("delta") is not None:
            print(f"{row['date']}: IV={row['implied_volatility']:.3f} delta={row['delta']:.3f} "
                  f"theta={row['theta']:.3f} dte={row['dte']}")
        else:
            print(f"{row['date']}: greeks unavailable (status={row['status']}), close={row['option_close']}")

# Chain snapshot — scan every near-the-money call on an underlying at once.
# NOTE: option_ticker (if used) takes the BARE OCC ticker, no "O:" prefix. Contracts are at data[0].results.
resp = requests.get(f"{base}/api/v1/options/chain",
    params={"symbol": "AAPL", "contract_type": "call",
            "min_strike_price": 290, "max_strike_price": 310, "limit": 50},
    headers={"X-API-Key": key})
body = resp.json()
if body.get("success") and body.get("data"):
    for c in body["data"][0]["results"]:
        d, g, dd = c["details"], c["greeks"], c["daily_data"]
        print(f"{d['symbol']} K={d['strike_price']} exp={d['expiration_date']} "
              f"close={dd['close']} IV={c['implied_volatility']:.3f} "
              f"delta={g['delta']:.3f} OI={c.get('open_interest', 0)}")
    if body["pagination"].get("has_more"):
        next_cursor = body["pagination"]["cursor"]  # pass as `cursor` for the next page
```
