---
name: arrays-data-api-macro-and-economics
description: Guides the agent to call Arrays REST APIs for macro and economics data (treasury rates, economic calendar/indicators, CPI, GDP, unemployment, inflation, consumer sentiment, macro index/forex/commodity, VIX). Use when the user asks about macroeconomic indicators, CPI release dates, economic data announcements, interest rates, forex, commodity prices (gold GCUSD, silver SILUSD, oil CLUSD), market index data (S&P 500 ^SPX, Dow Jones ^DJI, Nasdaq ^IXIC), or VIX volatility indexes.
---


# Arrays Data API — Macro and Economics

**Domain**: `macro_and_economics_data`. Treasury rates, economic calendar, economic indicators, macro index/forex/commodity historical and real-time data, and VIX.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Response envelope

All endpoints return a unified JSON envelope:
```json
{ "success": true, "request_id": "...", "data": [ ... ] }
```
- `data` is **always an array** (even for single-object results).
- Access data in Python: `body["data"]`
- Always check `body["success"]` before accessing data.

## Path prefix and endpoints

### Macro prefix — `/api/v1/macro/`
- **Paths** (all GET):
  - `economic-indicators` — economic indicators (CPI, GDP, unemployment, etc.)
  - `index/historical` — index historical data
  - `index/real-time` — index real-time data
  - `index/symbols` — available index symbols
  - `forex/historical` — forex historical data
  - `forex/real-time` — forex real-time data
  - `forex/symbols` — available forex symbols
  - `commodity/historical` — commodity historical data
  - `commodity/real-time` — commodity real-time data
  - `commodity/symbols` — available commodity symbols
  - `treasury-rates` — US treasury yield rates

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `macro/economic-indicators` | `economic-indicators` | 2. Economic indicators |
| GET | `macro/index/historical` | `macro-index-historical` | 3. Historical data |
| GET | `macro/forex/historical` | `macro-forex-historical` | 3. Historical data |
| GET | `macro/commodity/historical` | `macro-commodity-historical` | 3. Historical data |
| GET | `macro/index/real-time` | `macro-index-real-time` | 4. Real-time data |
| GET | `macro/forex/real-time` | `macro-forex-real-time` | 4. Real-time data |
| GET | `macro/commodity/real-time` | `macro-commodity-real-time` | 4. Real-time data |
| GET | `macro/forex/symbols` | `macro-forex-symbol-list` | 5. Symbol lists |
| GET | `macro/commodity/symbols` | `macro-commodity-symbol-list` | 5. Symbol lists |
| GET | `macro/treasury-rates` | `rates` | 7. Treasury rates |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


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
