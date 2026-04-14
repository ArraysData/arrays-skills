---
name: arrays-data-api-equity-estimates-and-targets
description: Calls Arrays REST APIs for equity estimates and price targets — analyst price target news/consensus/summary, FactSet consensus estimates (EPS, SALES, EBITDA, etc.), and company earnings guidance. Use when the user asks about analyst price targets, Wall Street earnings estimates, revenue forecasts, or company guidance. NOT for stock letter-grade quality ratings — use stock-technical-metrics for those.
---


# Arrays Data API — Equity Estimates and Targets

**Domain**: `equity_estimates_and_targets`. Price target news, price target consensus, price target summary, and FactSet estimates & guidance.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `company/price-target-news` | `company-price-target-news` | Price target news |
| GET | `company/price-target-consensus` | `company-price-target-consensus` | Price target consensus |
| GET | `company/price-target-summary` | `company-price-target-summary` | Price target summary |
| GET | `estimates-guidance` | `estimates-guidance` | Estimates & guidance |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Response format

All endpoints return a unified envelope with a **`data` array**:
```json
{ "success": true, "request_id": "...", "data": [ ... ] }
```
Access in Python: `body["data"]`

## Python example

```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# Price target news — use body["data"]
resp = requests.get(f"{base}/api/v1/stocks/company/price-target-news",
    params={"symbol": "AAPL", "start_time": 1704067200, "end_time": 1735689600, "limit": 20},
    headers={"X-API-Key": key})
body = resp.json()
news = body["data"]  # flat array of price target news items
for n in news:
    print(f"{n['analyst_company']}: ${n['price_target']}")

# Price target consensus — use body["data"]
resp = requests.get(f"{base}/api/v1/stocks/company/price-target-consensus",
    params={"symbol": "AAPL"},
    headers={"X-API-Key": key})
body = resp.json()
consensus = body["data"][0]  # single object in data array
print(f"Consensus: ${consensus['target_consensus']}, High: ${consensus['target_high']}")

# Estimates as of a specific date
# "What was the AAPL revenue estimate for fiscal year 2025 on June 28, 2025?"
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York")
start_ts = int(datetime(2025, 6, 28, tzinfo=ET).timestamp())
end_ts = int(datetime(2025, 6, 29, tzinfo=ET).timestamp())
resp = requests.get(f"{base}/api/v1/stocks/estimates-guidance",
    params={"symbol": "AAPL", "metrics": "SALES", "type": "estimate",
            "period_type": "annual", "fiscal_year": 2025,
            "start_time": start_ts, "end_time": end_ts,
            "limit": 50},
    headers={"X-API-Key": key})
body = resp.json()
estimates = body["data"]  # flat array of estimate rows
# Pick the row with the most analysts
best = max(estimates, key=lambda e: e.get("estimate_count") or 0)
print(f"FY{best.get('fiscal_year')}: mean={best.get('mean')}, count={best.get('estimate_count')}")
```
