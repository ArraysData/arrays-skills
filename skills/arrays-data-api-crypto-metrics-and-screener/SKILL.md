---
name: arrays-data-api-crypto-metrics-and-screener
description: Calls Arrays REST APIs for crypto on-chain analytics and screening — market cap, circulating/total supply, fear & greed index, on-chain metrics (MVRV, NUPL, SOPR, realized price, leverage ratio, SSR, whale ratio, Puell multiple, miner-to-exchange, inflow CDD), crypto metrics screener, token lists, trading pairs, token unlock schedules (cliff and linear allocations for DeFi protocols like Hyperliquid, Arbitrum, Uniswap, etc.), and Bitcoin correlation indices. Use when the user asks about crypto market cap, token supply, crypto market sentiment, on-chain analysis, token screening, token discovery, protocol token unlock events and vesting schedules, or Bitcoin correlation with other assets.
---


# Arrays Data API — Crypto Metrics and Screener

Market cap, supply, on-chain analytics (MVRV, NUPL, SOPR, etc.), fear & greed, crypto screener, token lists, trading pairs, DeFi pools.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `fear-greed-index` | `fear-greed-index` | Fear & greed index |
| GET | `unlock-events` | `unlock-events` | Unlock events |
| GET | `market-metrics` | `market-metrics` | Retrieve a specific metric for a given token (e.g. BTC's MA_20, MARKET_CAP, PRICE_CHANGE) |
| GET | `metrics/mvrv` | `metrics-mvrv` | Retrieve MVRV ratio for a given token |
| GET | `metrics/realized-price` | `metrics-realized-price` | Retrieve realized price for a given token |
| GET | `metrics/nupl` | `metrics-nupl` | Retrieve NUPL for a given token |
| GET | `metrics/leverage-ratio` | `metrics-leverage-ratio` | Retrieve leverage ratio for a given token |
| GET | `metrics/ssr` | `metrics-ssr` | Retrieve SSR for a given token |
| GET | `metrics/whale-ratio` | `metrics-whale-ratio` | Retrieve whale ratio for a given token |
| GET | `metrics/inflow-cdd` | `metrics-inflow-cdd` | Retrieve inflow CDD for a given token |
| GET | `metrics/miner-to-exchange` | `metrics-miner-to-exchange` | Retrieve miner-to-exchange flow for a given token |
| GET | `metrics/sopr` | `metrics-sopr` | Retrieve SOPR for a given token |
| GET | `metrics/puell-multiple` | `metrics-puell-multiple` | Retrieve Puell multiple for a given token |
| GET | `trading-pair` | `trading-pair` | Trading pair |
| GET | `list` | `list` | Token list by chain |
| GET | `market-cap` | `crypto-market-cap` | Retrieve market cap history for a given token |
| GET | `supply` | `crypto-supply` | Retrieve supply history for a given token |
| GET | `screener/metrics` | `screener-metrics` | Screener: find/filter/screen tokens by a metric (e.g. top tokens by market cap, tokens with RSI > 70) |
| GET | `screener/metrics/timerange` | `screener-metrics-timerange` | Screener: same as above but over a time range |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Response format

**Success** — `data` is always an array:
```json
{ "success": true, "data": [...], "request_id": "..." }
```

**Error**:
```json
{ "success": false, "data": null, "error": { "code": "...", "message": "..." }, "request_id": "..." }
```

## Pagination

- `list`: Offset-based. Use `offset` + `limit`.

## Python examples

```python
import requests, os, calendar
from datetime import datetime, timezone

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]
headers = {"X-API-Key": key}

def to_ts(year, month, day):
    return int(calendar.timegm(datetime(year, month, day, tzinfo=timezone.utc).timetuple()))

# On-chain metric: MVRV for BTC
resp = requests.get(f"{base}/api/v1/crypto/metrics/mvrv",
    params={"symbol": "BTC", "start_time": to_ts(2025, 1, 1), "end_time": to_ts(2025, 7, 1), "limit": 30},
    headers=headers)
body = resp.json()
if body["success"]:
    for item in body["data"]:  # V2 format: flat data array
        print(f"MVRV: {item['mvrv_ratio']}")

# Token unlock events for Arbitrum
resp = requests.get(f"{base}/api/v1/crypto/unlock-events",
    params={"token_id": "arbitrum", "start": "2025-01-01", "end": "2025-12-31"},
    headers=headers)
body = resp.json()
for event in body.get("data", []):
    if event.get("cliff_unlocks"):
        print(f"Cliff unlock: {event['cliff_unlocks']['cliff_amount']} tokens")
    if event.get("linear_unlocks"):
        print(f"Linear unlock: {event['linear_unlocks']['linear_amount']} tokens")

# Market cap
resp = requests.get(f"{base}/api/v1/crypto/market-cap",
    params={"symbol": "BTC", "start_time": to_ts(2025, 11, 1), "end_time": to_ts(2025, 11, 2)},
    headers=headers)
body = resp.json()
for item in body["data"]:
    print(f"Market Cap: ${item['market_cap']:,.0f}")

# Token supply
resp = requests.get(f"{base}/api/v1/crypto/supply",
    params={"symbol": "BTC", "start_time": to_ts(2025, 11, 1), "end_time": to_ts(2025, 11, 2)},
    headers=headers)
body = resp.json()
for item in body["data"]:
    print(f"Circulating: {item['circulating_supply']}, Total: {item['total_supply']}")
```

## Bitcoin Correlation with Other Assets

To compute the correlation between Bitcoin and another asset (e.g., TLT, SPY, gold), fetch kline data for both assets, align on common dates, and compute **Pearson correlation of price levels** (NOT returns).

**Steps**:
1. Fetch BTC daily kline from `/api/v1/crypto/kline` (use `symbol=BTC`)
2. Fetch the other asset's daily kline from `/api/v1/stocks/kline` (for stocks/ETFs like TLT, use `ticker=TLT`)
3. Build date→close_price maps for both
4. Find common dates (dates where both have data). TLT only trades on business days — use only dates present in BOTH datasets
5. Compute **Pearson correlation of the closing price series** (price levels, NOT returns)

**CRITICAL**: Use **price levels** for correlation, NOT daily returns. This is the standard methodology for the Bitcoin correlation index.

```python
import requests, os, calendar, math
from datetime import datetime, timezone

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

def to_ts(y, m, d):
    return int(calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple()))

# 30-day window ending Sep 28, 2025
start = to_ts(2025, 8, 28)
end = to_ts(2025, 9, 29)

# Fetch BTC kline
resp1 = requests.get(f"{base}/api/v1/crypto/kline",
    params={"symbol": "BTC", "start_time": start, "end_time": end, "interval": "1d", "limit": 40},
    headers={"X-API-Key": key})
btc_data = resp1.json()["data"]

# Fetch TLT kline (ETF — use stocks endpoint)
resp2 = requests.get(f"{base}/api/v1/stocks/kline",
    params={"symbol": "TLT", "start_time": start, "end_time": end, "interval": "1d", "limit": 40},
    headers={"X-API-Key": key})
tlt_data = resp2.json()["data"]

# Build date -> close maps
btc_prices = {c["time_period_start"][:10]: c["price_close"] for c in btc_data}
tlt_prices = {c["time_period_start"][:10]: c["price_close"] for c in tlt_data}

# Common dates only (align on trading days)
common = sorted(set(btc_prices) & set(tlt_prices))
btc_vals = [btc_prices[d] for d in common]
tlt_vals = [tlt_prices[d] for d in common]

# Pearson correlation of PRICE LEVELS
n = len(btc_vals)
mean_b = sum(btc_vals) / n
mean_t = sum(tlt_vals) / n
cov = sum((btc_vals[i] - mean_b) * (tlt_vals[i] - mean_t) for i in range(n)) / n
std_b = (sum((x - mean_b)**2 for x in btc_vals) / n) ** 0.5
std_t = (sum((x - mean_t)**2 for x in tlt_vals) / n) ** 0.5
corr = cov / (std_b * std_t)
print(f"{corr:.4f}")
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
