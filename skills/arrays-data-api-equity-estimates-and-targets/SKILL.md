---
name: arrays-data-api-equity-estimates-and-targets
description: Calls Arrays REST APIs for equity estimates and price targets — analyst price target news/consensus/summary, FactSet consensus estimates (EPS, SALES, EBITDA, etc.), and company earnings guidance. Use when the user asks about analyst price targets, Wall Street earnings estimates, revenue forecasts, or company guidance. NOT for stock letter-grade quality ratings — use stock-technical-metrics for those.
---

# Arrays Data API — Equity Estimates and Targets

**Domain**: `equity_estimates_and_targets`. Price target news, price target consensus, price target summary, and FactSet estimates & guidance.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Endpoints

All under prefix `/api/v1/stocks/` (all GET):

| Path | Description |
|------|-------------|
| `company/price-target-news` | Analyst price target news articles |
| `company/price-target-consensus` | Analyst price target consensus (high, low, median, consensus) |
| `company/price-target-summary` | Average target price over last month, quarter, year, and all time |
| `estimates-guidance` | FactSet consensus estimates or company guidance |

## Parameters by endpoint

### Price target news (`company/price-target-news`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | no | Stock symbol (e.g., META, AAPL) |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `limit` | integer | no | Maximum number of results (default: 20) |

**Response fields** (each item in `data` array)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol (e.g., `AAPL`) |
| `observedAt` | int64 | Observed timestamp (Unix seconds, may be omitted) |
| `publishTime` | string | Formatted time (`YYYY-MM-DD HH:mm:ss`, America/New_York, may be omitted) |
| `newsUrl` | string | Full URL to the news article |
| `newsTitle` | string | Title of the news article |
| `analystName` | string | Name of the analyst (may be omitted) |
| `analystCompany` | string | Company of the analyst (e.g., `Goldman Sachs`) |
| `priceTarget` | float64 | Price target value |
| `adjPriceTarget` | float64 | Adjusted price target value |
| `priceWhenPosted` | float64 | Stock price when the news was posted |
| `newsPublisher` | string | Publisher name (e.g., `StreetInsider`) |
| `newsBaseUrl` | string | Base URL of the publisher (e.g., `streetinsider.com`) |

### Price target consensus (`company/price-target-consensus`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (uppercase, e.g., META, AAPL) |

**Response fields** (single object in response)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `target_high` | float64 | Highest analyst price target |
| `target_low` | float64 | Lowest analyst price target |
| `target_consensus` | float64 | Consensus (average) analyst price target |
| `target_median` | float64 | Median analyst price target |

### Price target summary (`company/price-target-summary`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (uppercase, e.g., META, AAPL) |

**Response fields** (single object in response)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `last_month_count` | int32 | Number of analyst targets in the last month |
| `last_month_avg_price_target` | float64 | Average price target over the last month |
| `last_quarter_count` | int32 | Number of analyst targets in the last quarter |
| `last_quarter_avg_price_target` | float64 | Average price target over the last quarter |
| `last_year_count` | int32 | Number of analyst targets in the last year |
| `last_year_avg_price_target` | float64 | Average price target over the last year |
| `all_time_count` | int32 | Total number of analyst targets (all time) |
| `all_time_avg_price_target` | float64 | Average price target (all time) |
| `publishers` | string | Comma-separated list of publisher names |

### Estimates & guidance (`estimates-guidance`)

**IMPORTANT**: This endpoint returns multiple rows for the same fiscal period, each with a different `estimateDate` (the date the consensus was computed). The most recent row by `estimateDate` may be a stale partial update with only 1 analyst — do NOT blindly use the most recent row. Instead:
- When the question asks for the estimate **on a specific date** (e.g., "on June 28th, 2025"), use `observed_at_start` and `observed_at_end` to get the snapshot near that date: `observed_at_start=2025-06-28&observed_at_end=2025-06-29`.
- When the question asks for a specific fiscal period without a date, use `fiscal_year` and `fiscal_quarter` filters and pick the row with the highest `estimateCount` (most analysts contributing).

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (e.g., AAPL) |
| `metrics` | string | yes | Metrics (comma-separated). Supported: EPS, SALES, DPS, CFPS, EBITDA, EBIT, BPS, ASSETS |
| `type` | string | yes | Data type: `estimate` or `guidance` |
| `periodicity` | string | no | Periodicity (default: ANN). Values: `ANN`, `QTR`, `SEMI` |
| `observed_at_start` | string | no | Start date for observed_at filter (`YYYY-MM-DD`) |
| `observed_at_end` | string | no | End date for observed_at filter (`YYYY-MM-DD`) |
| `fiscal_year` | integer | no | Fiscal year filter (e.g., 2024) |
| `fiscal_quarter` | integer | no | Fiscal quarter filter (only valid when periodicity=QTR, 1-4) |
| `limit` | integer | no | Result limit (default: 10, max: 1000) |

**Response fields when `type=estimate`** (each item in `data` array is a `FactsetEstimateRow`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `fsymId` | string | FactSet symbol ID |
| `metric` | string | Metric name (e.g., EPS, SALES, EBITDA) |
| `periodicity` | string | Periodicity: `ANN`, `QTR`, or `SEMI` |
| `fiscalPeriod` | *int32 | Fiscal period (Q1=1, Q2=2, Q3=3, Q4=4) |
| `fiscalYear` | *int32 | Fiscal year |
| `fiscalEndDate` | string | Fiscal period end date (`YYYY-MM-DD`) |
| `estimateDate` | string | Estimate adjustment date (`YYYY-MM-DD`) |
| `observedAt` | string | Point-in-time observation timestamp (ISO 8601) |
| `mean` | *float64 | Mean estimate |
| `median` | *float64 | Median estimate |
| `standardDeviation` | *float64 | Standard deviation |
| `high` | *float64 | High estimate |
| `low` | *float64 | Low estimate |
| `estimateCount` | *int32 | Number of estimates |
| `up` | *int32 | Number of estimates increased |
| `down` | *int32 | Number of estimates decreased |

**Response fields when `type=guidance`** (each item in `data` array is a `FactsetGuidanceRow`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `fsymId` | string | FactSet symbol ID |
| `metric` | string | Metric name (e.g., EPS, SALES, EBITDA) |
| `periodicity` | string | Periodicity: `ANN`, `QTR`, or `SEMI` |
| `fiscalPeriod` | *int32 | Fiscal period |
| `fiscalYear` | *int32 | Fiscal year |
| `fiscalEndDate` | string | Fiscal period end date |
| `guidanceDate` | string | Guidance date (`YYYY-MM-DD`) |
| `observedAt` | string | Point-in-time observation timestamp |
| `guidanceRange` | string | Guidance range string (e.g., `5.00 - 5.50`, may be omitted) |
| `guidanceLow` | *float64 | Guidance low value |
| `guidanceHigh` | *float64 | Guidance high value |
| `guidanceMidpoint` | *float64 | Guidance midpoint |
| `prevMidpoint` | *float64 | Previous guidance midpoint |
| `prevLow` | *float64 | Previous guidance low |
| `prevHigh` | *float64 | Previous guidance high |
| `meanBefore` | *float64 | Consensus mean before guidance |
| `meanSurpriseAmt` | *float64 | Surprise amount vs mean |
| `meanSurpriseAmtRatio` | *float64 | Surprise ratio vs mean (decimal, not percentage) |

## Response format

Endpoints use **two different** response wrappers:

**V2 format** (price-target-news, estimates-guidance) — data in `data` field:
```json
{ "success": true, "data": [ ... ] }
```
Access in Python: `body["data"]`

**Standard format** (price-target-consensus, price-target-summary) — data in `response` field:
```json
{ "success": true, "response": { "symbol": "AAPL", "target_high": 200, ... } }
```
Access in Python: `body["response"]`

## Python example

```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# Price target news (V2 format — use body["data"])
resp = requests.get(f"{base}/api/v1/stocks/company/price-target-news",
    params={"symbol": "AAPL", "start_time": 1704067200, "end_time": 1735689600, "limit": 20},
    headers={"X-API-Key": key})
body = resp.json()
news = body["data"]  # flat array of price target news items
for n in news:
    print(f"{n['analystCompany']}: ${n['priceTarget']}")

# Price target consensus (Standard format — use body["response"])
resp = requests.get(f"{base}/api/v1/stocks/company/price-target-consensus",
    params={"symbol": "AAPL"},
    headers={"X-API-Key": key})
body = resp.json()
consensus = body["response"]  # single object
print(f"Consensus: ${consensus['target_consensus']}, High: ${consensus['target_high']}")

# Estimates as of a specific date — use observed_at to get the right snapshot
# "What was the AAPL revenue estimate on June 28, 2025?"
resp = requests.get(f"{base}/api/v1/stocks/estimates-guidance",
    params={"symbol": "AAPL", "metrics": "SALES", "type": "estimate",
            "periodicity": "QTR",
            "observed_at_start": "2025-06-28",  # target date
            "observed_at_end": "2025-06-29",    # next day
            "limit": 50},
    headers={"X-API-Key": key})
body = resp.json()
estimates = body["data"]  # flat array of estimate rows
# Pick the row with the most analysts (highest estimateCount)
best = max(estimates, key=lambda e: e.get("estimateCount") or 0)
print(f"FY{best.get('fiscalYear')} Q{best.get('fiscalPeriod')}: "
      f"mean={best.get('mean')}, count={best.get('estimateCount')}")
```
