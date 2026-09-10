---
name: arrays-data-api-macro-and-economics
description: Guides the agent to call Arrays REST APIs for macro and economics data (treasury rates, economic indicators, CPI, GDP, unemployment, inflation, consumer sentiment, macro index/forex/commodity, VIX). Use when the user asks about macroeconomic indicators, CPI release dates, economic data announcements, interest rates, forex, commodity prices (gold GCUSD, silver SILUSD, oil CLUSD), market index data (S&P 500 ^SPX, Dow Jones ^DJI, Nasdaq ^IXIC), or VIX volatility indexes.
---


# Arrays Data API — Macro and Economics

**Domain**: `macro_and_economics_data`. Treasury rates, economic indicators, macro index/forex/commodity historical and real-time data, and VIX.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.arrays.org`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Response envelope

All endpoints return a unified JSON envelope:
```json
{ "success": true, "request_id": "...", "data": [ ... ] }
```
- `data` is **always an array** (even for single-object results).
- Access data in Python: `body["data"]`
- Always check `body["success"]` before accessing data.

On failure the shape is different — `data` is `null` and the reason is in `error`:
```json
{ "success": false, "data": null,
  "error": { "code": "INVALID_PARAMETER",
             "message": "forex symbol not found: eurusd",
             "docs_url": "https://data-tools.prd.arrays.org/docs/output/v1_macro_forex_real-time_get.json" },
  "request_id": "..." }
```
An unknown symbol is 400 / `INVALID_PARAMETER`, not 404. Read `error.message` before retrying.

## Endpoints

- **Prefix**: `/api/v1/macro/`

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `economic-indicators` | `economic-indicators` | Economic indicators (CPI, GDP, unemployment, etc.) |
| GET | `index/historical` | `macro-index-historical` | Index historical data |
| GET | `forex/historical` | `macro-forex-historical` | Forex historical data |
| GET | `commodity/historical` | `macro-commodity-historical` | Commodity historical data |
| GET | `index/real-time` | `macro-index-real-time` | Index real-time data |
| GET | `forex/real-time` | `macro-forex-real-time` | Forex real-time data |
| GET | `commodity/real-time` | `macro-commodity-real-time` | Commodity real-time data |
| GET | `index/symbols` | `macro-index-symbol-list` | Available index symbols (the index roster) |
| GET | `forex/symbols` | `macro-forex-symbol-list` | Available forex symbols |
| GET | `commodity/symbols` | `macro-commodity-symbol-list` | Available commodity symbols |
| GET | `treasury-rates` | `rates` | US treasury yield rates |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.

Discover valid symbols with the matching `*/symbols` endpoint first.

## Example

```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# Economic indicators — get US CPI
resp = requests.get(f"{base}/api/v1/macro/economic-indicators",
    params={"indicator_type": "CPI", "time_type": "CALENDAR_START_DATE",
            "start_time": 1719792000, "end_time": 1722470400},
    headers={"X-API-Key": key})
body = resp.json()
obs = body["data"][0]["observations"]  # data is array, take first element
print(obs[0]["date"], obs[0]["value"])

# Commodity historical — get gold price
resp = requests.get(f"{base}/api/v1/macro/commodity/historical",
    params={"symbol": "GCUSD", "start_time": 1746057600, "end_time": 1746057600},
    headers={"X-API-Key": key})
body = resp.json()
bars = body["data"]  # array of OHLCV bars
print(bars[0]["close"])

# Treasury rates
resp = requests.get(f"{base}/api/v1/macro/treasury-rates",
    params={"start_time": to_ts(2025, 1, 1), "end_time": to_ts(2025, 3, 1)},
    headers={"X-API-Key": key})
body = resp.json()
rates = body["data"][0]["rates"]  # nested: body["data"][0] has {"rates": [...]}
print(rates[0]["year10"])

```
