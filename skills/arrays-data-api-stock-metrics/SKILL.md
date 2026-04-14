---
name: arrays-data-api-stock-metrics
description: Guides the agent to call Arrays REST APIs for stock metrics — financial metrics (revenue TTM, net income TTM, EPS TTM, ROE, ROA, ROIC, margins, debt ratios, current/quick ratio), market/technical metrics (market cap, moving averages, EMA, SMA, RSI, MACD, Bollinger, VWAP, beta, volatility, PE ratio, PB ratio, PS ratio, dividend yield, enterprise value, EV/EBITDA, price changes), darkpool OHLC, and PIT ratings. Use when the user asks about stock market cap, financial ratios, computed market indicators, darkpool data, or point-in-time stock quality ratings (letter-grade scores like A+, B, C based on DCF, ROE, P/E, etc.).
---


# Arrays Data API — Stock Metrics

**Domain**: `stock_metrics`. Financial metrics, market/technical metrics, darkpool OHLC data, and analyst ratings.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Path prefix and endpoints

- **Prefix**: `/api/v1/stocks/`
- **Paths** (all GET):
  - `financial-metrics` — financial metrics (revenue TTM, EPS TTM, ROE, margins, debt ratios, etc.)
  - `market-metrics` — stock market metrics (beta, PE, volatility, etc.)
  - `darkpool` — darkpool OHLC data
  - `ratings` — analyst ratings (PIT)

## Response format

All endpoints return data in the `data` array:
```json
{ "success": true, "data": [...], "request_id": "..." }
```
Access in Python: `body["data"]`

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `financial-metrics` | `financial-metrics` | Fundamental ratios from financial statements (revenue TTM, EPS TTM, ROE, margins, debt ratios). Response: `data[].{symbol, metric, values[]}` where `values[].{observed_at, value, period, fiscal_year}` |
| GET | `market-metrics` | `market-metrics` | Technical/market indicators from price data (market cap, MA, EMA, RSI, MACD, beta, PE ratio, etc.). Response: `data[].{symbol, type, values[]}` where `values[].{observed_at, date, value}` |
| GET | `darkpool` | `darkpool` | Darkpool OHLC data |
| GET | `ratings` | `ratings` | PIT analyst ratings |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.

## Python examples

```python
import requests, os, calendar
from datetime import datetime, timezone

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

def to_ts(year, month, day, hour=0):
    return int(calendar.timegm(datetime(year, month, day, hour, tzinfo=timezone.utc).timetuple()))

# Financial metrics — AAPL revenue TTM
resp = requests.get(f"{base}/api/v1/stocks/financial-metrics",
    params={"metric": "REVENUE_TTM", "symbol": "AAPL",
            "start_time": to_ts(2025, 1, 1), "end_time": to_ts(2025, 6, 1)},
    headers={"X-API-Key": key})
body = resp.json()
for entry in body["data"]:
    latest = entry["values"][0]  # most recent first
    print(f"{entry['symbol']} {entry['metric']}: {latest['value']} (FY{latest['fiscal_year']} {latest['period']})")

# Market metrics — AAPL 20-day moving average
resp = requests.get(f"{base}/api/v1/stocks/market-metrics",
    params={"symbol": "AAPL", "indicator": "MA_20", "interval": "1d",
            "start_time": to_ts(2025, 12, 1), "end_time": to_ts(2025, 12, 5)},
    headers={"X-API-Key": key})
body = resp.json()
for item in body["data"]:
    for v in item["values"]:
        print(f"{v['date']}: {v['value']}")

# Darkpool trades at a specific hour
resp = requests.get(f"{base}/api/v1/stocks/darkpool",
    params={"symbol": "TSLA", "start_time": to_ts(2025, 12, 4), "end_time": to_ts(2025, 12, 5)},
    headers={"X-API-Key": key})
body = resp.json()
entries = body["data"]
target_ts = to_ts(2025, 12, 4, 18)  # 18:00 UTC
for e in entries:
    if e["timestamp"] == target_ts:
        print(f"Trade count at 18:00 UTC: {e['trade_count']}")

# Ratings
resp = requests.get(f"{base}/api/v1/stocks/ratings",
    params={"symbol": "AAPL", "start_time": to_ts(2025, 1, 1), "end_time": to_ts(2025, 12, 31)},
    headers={"X-API-Key": key})
body = resp.json()
for r in body["data"]:
    print(f"{r['date']}: Rating {r['rating']} (score: {r['overall_score']})")
```
