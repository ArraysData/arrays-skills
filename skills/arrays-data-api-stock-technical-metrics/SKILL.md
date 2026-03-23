---
name: arrays-data-api-stock-technical-metrics
description: Guides the agent to call Arrays REST APIs for stock technical metrics (market metrics, darkpool, PIT ratings). Use when the user needs stock market-level metrics, darkpool OHLC data, or point-in-time stock quality ratings (letter-grade scores like A+, B, C based on DCF, ROE, P/E, etc.).
---

# Arrays Data API — Stock Technical Metrics

**Domain**: `stock_technical_metrics`. Stock market metrics, darkpool OHLC data, and analyst ratings.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Path prefix and endpoints

- **Prefix**: `/api/v1/stocks/`
- **Paths** (all GET):
  - `market-metrics` — stock market metrics (beta, PE, volatility, etc.)
  - `darkpool` — darkpool OHLC data
  - `ratings` — analyst ratings (PIT)

## Response format

**V2 format** (market-metrics, ratings) — data in `data` field:
```json
{ "success": true, "data": [ ... ] }
```
Access in Python: `body["data"]`

**Standard nested format** (darkpool) — data in `response.data` field:
```json
{ "success": true, "response": { "data": [ ... ] } }
```
Access in Python: `body["response"]["data"]`

## Parameters by endpoint

### Market Metrics (`market-metrics`)

Retrieve time series data for various market indicators, including technical and fundamental metrics.

**Indicator formats** — indicators requiring a period are formatted as `{INDICATOR}_{PERIOD}`:
- **PRICE_CHANGE**: `PRICE_CHANGE_1d`, `PRICE_CHANGE_1w`, `PRICE_CHANGE_1M`, `PRICE_CHANGE_3M`, `PRICE_CHANGE_6M`, `PRICE_CHANGE_ytd`, `PRICE_CHANGE_1y`, `PRICE_CHANGE_3y`, `PRICE_CHANGE_5y`
- **MA**: `MA_5`, `MA_10`, `MA_20`, `MA_60`, `MA_120`, `MA_200`
- **EMA**: `EMA_5`, `EMA_10`, `EMA_20`, `EMA_60`, `EMA_120`, `EMA_200`
- **VOLATILITY**: `VOLATILITY_20`, `VOLATILITY_60`, `VOLATILITY_90`
- **RSI**: `RSI_14`
- **MACD**: `MACD_12,26,9`
- **BOLLINGER**: `BOLLINGER_20,2`
- **VWAP**: `VWAP_DAY`
- **BETA**: `BETA` (default period `SPX_252`; interval must be `1d`)
- **AVERAGE_DAILY_DOLLAR_VOLUME**: `AVERAGE_DAILY_DOLLAR_VOLUME` (default period `20`; interval must be `1d`)
- **Fundamentals**: `MARKET_CAP`, `PE_RATIO`, `PS_RATIO`, `PB_RATIO`, `DIVIDEND_YIELD`, `ENTERPRISE_VALUE`, `EV_EBITDA_RATIO`

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interval` | string | yes | Time interval |
| `indicator` | string | yes | Indicator type (e.g., MA_20, PRICE_CHANGE_1d) |
| `symbol` | string | no | Stock symbol (optional, e.g., AAPL) |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |

**Response fields** (in `data` array — each element is a `MarketSymbolMetricData`):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol (e.g., AAPL) |
| `type` | string | Indicator type (e.g., MA_20) |
| `values` | array | Array of time series data points |

Each element in `values` (`MarketMetricValue`):

| Field | Type | Description |
|-------|------|-------------|
| `observedAt` | int64 | Observation timestamp (Unix seconds) |
| `date` | string | Formatted date (YYYY-MM-DD HH:mm:ss, UTC+0) |
| `value` | *float64 | Metric value (null if not available) |
| `metricComponent` | string | Metric component label (e.g., UPPER); omitted when empty |

---

### Darkpool (`darkpool`)

Retrieve darkpool trading data for specified stock tickers within a time range. Returns hourly aggregated OHLC and volume data.

**IMPORTANT**: Data is aggregated hourly. The `timestamp` field represents the **start** of each hour in UTC. When looking for data at a specific hour (e.g., 18:00 UTC), compute the target hour-start timestamp using `datetime` and compare with equality. For example, 2025-12-04 18:00 UTC → `int(calendar.timegm(datetime(2025, 12, 4, 18, tzinfo=timezone.utc).timetuple()))`.

**IMPORTANT**: To get data for a full day including evening hours, set `end_date` to the **next day**. For example, to get all Dec 4 data, use `start_date=2025-12-04` and `end_date=2025-12-05`.

**IMPORTANT**: The darkpool response uses **Standard nested format**: `body["response"]["data"]`, NOT `body["data"]`.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | string | yes | Stock ticker symbol (e.g., AAPL) |
| `start_date` | string | yes | Start date in YYYY-MM-DD format |
| `end_date` | string | yes | End date in YYYY-MM-DD format (use next day to include full target day) |

**Response fields** (in `data` array — each element is a `DarkpoolOHLCData`):

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Stock ticker symbol |
| `timestamp` | int64 | Hourly timestamp (Unix seconds, UTC) — start of the hour |
| `open` | string | Opening price in the hour |
| `high` | string | Highest price in the hour |
| `low` | string | Lowest price in the hour |
| `close` | string | Closing price in the hour |
| `volume` | int64 | Total trading volume |
| `trade_count` | int32 | Number of trades executed |
| `total_value` | string | Total transaction value |
| `vwap` | string | Volume Weighted Average Price |

---

### Ratings (`ratings`)

Get Point-in-Time (PIT) stock ratings data for a specific symbol within a time range.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (e.g., AAPL, TSLA) |
| `start_time` | integer | yes | Start timestamp (Unix seconds, UTC) |
| `end_time` | integer | yes | End timestamp (Unix seconds, UTC) |
| `limit` | integer | no | Maximum number of results (1-1000, default: 50) |

**Response fields** (in `data` array — each element is a `PITStockRatingData`):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | Rating date (YYYY-MM-DD format) |
| `rating` | string | Overall rating (e.g., "A+", "B", "C") |
| `overallScore` | int32 | Overall composite score |
| `discountedCashFlowScore` | int32 | DCF model score |
| `returnOnEquityScore` | int32 | ROE score |
| `returnOnAssetsScore` | int32 | ROA score |
| `debtToEquityScore` | int32 | Debt-to-Equity ratio score |
| `priceToEarningsScore` | int32 | P/E ratio score |
| `priceToBookScore` | int32 | P/B ratio score |
| `publishTime` | int64 | Data publish timestamp (Unix seconds, UTC) |

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).

## Python examples

```python
import requests, os, calendar
from datetime import datetime, timezone

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

def to_ts(year, month, day, hour=0):
    return int(calendar.timegm(datetime(year, month, day, hour, tzinfo=timezone.utc).timetuple()))

# Darkpool trades at a specific hour (Standard nested format — body["response"]["data"])
resp = requests.get(f"{base}/api/v1/stocks/darkpool",
    params={"ticker": "TSLA", "start_date": "2025-12-04", "end_date": "2025-12-05"},
    headers={"X-API-Key": key})
body = resp.json()
entries = body["response"]["data"]  # Standard nested format
target_ts = to_ts(2025, 12, 4, 18)  # 18:00 UTC
for e in entries:
    if e["timestamp"] == target_ts:
        print(f"Trade count at 18:00 UTC: {e['trade_count']}")

# Ratings (V2 format — body["data"])
resp = requests.get(f"{base}/api/v1/stocks/ratings",
    params={"symbol": "AAPL", "start_time": to_ts(2025, 1, 1), "end_time": to_ts(2025, 12, 31)},
    headers={"X-API-Key": key})
body = resp.json()
for r in body["data"]:
    print(f"{r['date']}: Rating {r['rating']} (score: {r['overallScore']})")

# Market metrics (V2 format — body["data"])
resp = requests.get(f"{base}/api/v1/stocks/market-metrics",
    params={"symbol": "AAPL", "indicator": "MA_20", "interval": "1d",
            "start_time": to_ts(2025, 12, 1), "end_time": to_ts(2025, 12, 5)},
    headers={"X-API-Key": key})
body = resp.json()
for item in body["data"]:
    for v in item["values"]:
        print(f"{v['date']}: {v['value']}")
```
