---
name: arrays-data-api-stock-metrics
description: Guides the agent to call Arrays REST APIs for stock metrics — financial metrics (revenue TTM, net income TTM, EPS TTM, ROE, ROA, ROIC, margins, debt ratios, current/quick ratio), market/technical metrics (market cap, moving averages, EMA, SMA, RSI, MACD, Bollinger, VWAP, beta, volatility, PE ratio (incl. trailing P/E and forward P/E), PB ratio, PS ratio, dividend yield, enterprise value, EV/EBITDA, price changes), darkpool OHLC, and PIT ratings. Use when the user asks about stock market cap, financial ratios, computed market indicators (including trailing or forward P/E), darkpool data, or point-in-time stock quality ratings (letter-grade scores like A+, B, C based on DCF, ROE, P/E, etc.).
---


# Arrays Data API — Stock Metrics

**Domain**: `stock_metrics`. Financial metrics, market/technical metrics, darkpool OHLC data, and analyst ratings.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.arrays.org`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- **Data ordering**: `financial-metrics`, `market-metrics` and `ratings` are **newest-first** (descending by `observed_at` / `publish_time`). **Exception**: `darkpool` is **oldest-first** (ascending by `timestamp`), so its `data[0]` is the earliest hour in the range. Match by the time field rather than relying on `data[0]`.

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

## Computed P/E ratios (trailing & forward)

P/E is a `price / EPS` division.

- **Trailing P/E**: The `PE_RATIO` indicator on `market-metrics` already gives this directly — prefer it. Only compute manually when you need a custom as-of-date price or a non-standard TTM window: current price / `EPS_TTM` (`financial-metrics`, latest `values[0]`).
- **Forward P/E** = current price / **forward EPS estimate**.
  - Forward EPS comes from `estimates-guidance` (read the `arrays-data-api-equity-estimates-and-targets` skill for more details): `metrics=EPS`, `type=estimate`, `period_type=annual, semi-annual or quarterly`.
  - **Preferred forward window: the next 4 quarters' EPS estimates** (the current/in-progress quarter plus the following three, i.e. Q, Q+1, Q+2, Q+3) summed into a next-twelve-months (NTM) forward EPS. Query `period_type=quarterly`, keep the upcoming quarters, and sum the latest **median** consensus estimate for each (prefer `median` over `mean` — it's more robust to outlier analyst estimates). Other valid windows include current fiscal year, next fiscal year, etc. Match what the question needs.

For both, "current price" is the latest daily close from `stocks/kline` (in the `arrays-data-api-spot-market-price-and-volume` skill).

```python
# Forward P/E for AAPL — price / next-4-quarters (NTM) consensus EPS (preferred default)
# 1) latest daily close
resp = requests.get(f"{base}/api/v1/stocks/kline",
    params={"symbol": "AAPL", "interval": "1d",
            "start_time": to_ts(2026, 5, 25), "end_time": to_ts(2026, 6, 2)},
    headers={"X-API-Key": key})
price = resp.json()["data"][0]["price_close"]  # reverse-chronological; data[0] is latest

# 2) quarterly EPS estimates -> sum the next 4 quarters (current + Q+1, Q+2, Q+3)
resp = requests.get(f"{base}/api/v1/stocks/estimates-guidance",
    params={"symbol": "AAPL", "metrics": "EPS", "type": "estimate",
            "period_type": "quarterly", "limit": 100},
    headers={"X-API-Key": key})
rows = [r for r in resp.json()["data"] if (r.get("estimate_count") or 0) > 3]
today = "2026-06-02"
upcoming = [r for r in rows if r["fiscal_end_date"] >= today]  # not-yet-reported quarters
next_quarters = sorted({r["fiscal_end_date"] for r in upcoming})[:4]  # nearest 4 quarters
# within each quarter, take the latest estimate by estimate_date, then sum the
# median consensus -> NTM EPS (median is more robust to outlier analyst estimates)
fwd_eps = sum(
    max((r for r in upcoming if r["fiscal_end_date"] == q),
        key=lambda e: e["estimate_date"])["median"]
    for q in next_quarters)

forward_pe = price / fwd_eps  # if only annual estimates exist, fall back to the FY consensus

# Trailing P/E (manual) — prefer the PE_RATIO market-metric unless you need a custom price/window
resp = requests.get(f"{base}/api/v1/stocks/financial-metrics",
    params={"metric": "EPS_TTM", "symbol": "AAPL",
            "start_time": to_ts(2025, 6, 1), "end_time": to_ts(2026, 6, 2)},
    headers={"X-API-Key": key})
eps_ttm = resp.json()["data"][0]["values"][0]["value"]
trailing_pe = price / eps_ttm
```

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
    for v in item["values"]:  # values sorted newest first (descending by observed_at)
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
