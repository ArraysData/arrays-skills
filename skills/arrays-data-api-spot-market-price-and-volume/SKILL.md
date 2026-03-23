---
name: arrays-data-api-spot-market-price-and-volume
description: Calls Arrays REST APIs for spot market prices and volume — stock and crypto candlestick/kline/OHLCV data, token details, market cap, circulating supply, and previous close. Use when the user asks for price history, price charts, candlestick data, current price, market capitalization, token supply, or price correlation between assets.
---

# Arrays Data API — Spot Market Price and Volume

Stock and crypto kline/OHLCV, token detail by symbol, market cap, supply, previous 24h close, and full bar data.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Important notes

- **Data ordering**: Kline results are returned in **reverse chronological order** (latest first). When querying for data "on" a specific date (e.g., `start_time=Aug12, end_time=Aug13`), `data[0]` is the NEXT day's candle (Aug 13) and `data[-1]` is the target day (Aug 12). **Always match by `time_period_start` or use `data[-1]`** to get the target date's data point.
- **Timestamp computation**: Always use Python `datetime` + `calendar` to compute Unix timestamps. Do NOT calculate timestamps by mental arithmetic.
```python
import calendar
from datetime import datetime, timezone
ts = int(calendar.timegm(datetime(2025, 8, 13, 0, 0, 0, tzinfo=timezone.utc).timetuple()))
```

## Endpoints

**IMPORTANT**: For crypto price/volume queries using simple symbols like `BTC` or `ETH`, prefer `tokens/kline` over `tokens/ohlcv-full-bar-data`. The `ohlcv-full-bar-data` endpoint requires a valid Binance trading pair and may fail with "trading pair not found" for simple base symbols. Use `tokens/kline` with `symbol=BTC` or `symbol=ETH` which works reliably.

### Crypto — `/api/v1/tokens/`

| Method | Path | Description |
|--------|------|-------------|
| GET | `symbol` | Token detail by symbol |
| GET | `kline` | Crypto kline (candlestick) data (use this for BTC, ETH price queries) |
| GET | `ohlcv-full-bar-data` | Crypto OHLCV full bar data (requires specific trading pair) |
| GET | `futures/ohlcv-full-bar-data` | Crypto futures OHLCV data — use this for "futures trading volume" queries. `volume_traded` is in **quote currency (USDT)**, no conversion needed. Symbol format: `ETHUSDT`, `BTCUSDT` |
| GET | `previous-24-hours-close-price` | Crypto previous 24h close price |
| GET | `market-cap` | Token market cap history |
| GET | `supply` | Token supply history |

### Stocks v1 — `/api/v1/stocks/`

| Method | Path | Description |
|--------|------|-------------|
| GET | `kline` | Stock kline (candlestick) data |
| GET | `ohlcv-full-bar-data` | Stock OHLCV full bar data |
| GET | `previous-24-hours-close-price` | Stock previous 24h close price |

### Stocks v2 — `/api/v2/stocks/`

| Method | Path | Description |
|--------|------|-------------|
| GET | `kline` | Stock OHLC data (dedicated kline service) |

## Parameters by endpoint

### Kline endpoints (`tokens/kline`, `stocks/kline`, `tokens/ohlcv-full-bar-data`, etc.)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` (crypto) / `ticker` (stocks) | string | yes | Token symbol (e.g. `BTC`, `ETH`) or stock ticker (e.g. `AAPL`, `TSLA`) |
| `start_time` | int | yes | Start time (Unix seconds). Must be > 0 |
| `end_time` | int | yes | End time (Unix seconds). Must be > start_time |
| `interval` | string | yes | Time interval: `1min`, `2min`, `3min`, `5min`, `10min`, `15min`, `30min`, `45min`, `1h`, `2h`, `4h`, `1d`, `1w`, `1m`, `3m`, `6m` |
| `limit` | int | yes | Max data points. `tokens/kline`: default 500, max 1000. `ohlcv-full-bar-data` and `stocks/kline`: default 5000, max 10000 |
| `cursor` | string | no | Pagination cursor (only for `tokens/kline`) |

### Token detail (`tokens/symbol`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (e.g. `BTC`, `ETH`) |
| `interval` | string | no | Time window: `1min`, `15min`, `60min`, `24h` (default `24h`) |
| `start_time` | int | no | Unix seconds (alternative to interval) |
| `end_time` | int | no | Unix seconds (alternative to interval) |

### Previous 24h close (`tokens/previous-24-hours-close-price`, `stocks/previous-24-hours-close-price`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol or stock ticker |
| `timestamp` | int | yes | Unix seconds (UTC) |

### Market cap & supply (`tokens/market-cap`, `tokens/supply`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (e.g. `BTC`, `ETH`) |
| `start_time` | int | yes | Unix seconds, must be > 0 |
| `end_time` | int | yes | Unix seconds, must be > 0 |
| `interval` | string | no | Day-level or above only (e.g. `1d`, `7d`, `30d`) |

### V2 stocks kline (`v2/stocks/kline`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (e.g. `AAPL`, `TSLA`) |
| `start_time` | int | yes | Start time (Unix seconds) |
| `end_time` | int | yes | End time (Unix seconds) |
| `interval` | string | yes | `1min`, `5min`, `15min`, `30min`, `45min`, `1h`, `4h`, `1d`, `1w`, `1m` |
| `limit` | int | no | Max data points (default 100) |

## Response format

**Standard** (kline, previous-close, token detail):
```json
{ "success": true, "response": [...], "total": 42, "request_id": "..." }
```

**V2** (ohlcv-full-bar-data, market-cap, supply):
```json
{ "success": true, "data": [...], "request_id": "..." }
```

**Error**:
```json
{ "success": false, "error": { "code": "INVALID_TIMESTAMP", "message": "..." }, "request_id": "..." }
```

Always check `success` before reading `response` or `data`.

## Response fields by endpoint

### Crypto kline — `tokens/kline`

Wrapper: `APIResponse` -- the `response` field contains the object below.

**Top-level response object:**

| Field | Type | Description |
|-------|------|-------------|
| `data` | array | Array of kline data items (see below) |
| `count` | integer | Number of data points returned in this response |
| `cursor` | string | Pagination cursor for the next page; empty if no more data |

**Each item in `data` (KlineData):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Time open | `time_open` | integer | K-line open time (Unix timestamp, seconds, UTC) |
| Time close | `time_close` | integer | K-line close time (Unix timestamp, seconds, UTC) |
| Period start | `time_period_start` | string | Open time in RFC 3339 format (e.g. `"2024-07-24T00:00:00Z"`) |
| Period end | `time_period_end` | string | Close time in RFC 3339 format |
| Open price | `price_open` | number | Opening price |
| Close price | `price_close` | number | Closing price |
| Low price | `price_low` | number | Lowest price in the interval |
| High price | `price_high` | number | Highest price in the interval |
| Trades count | `trades_count` | integer | Number of trades in the interval |
| Volume traded | `volume_traded` | number | Quote-currency trading volume |

### Crypto OHLCV full bar — `tokens/ohlcv-full-bar-data`

Wrapper: `APIResponseV2` -- the `data` field is a flat array of KlineData items.

**Response fields:** Same KlineData fields as `tokens/kline` above (no cursor, no wrapping object -- just the array directly in `data`).

### Crypto futures OHLCV full bar — `tokens/futures/ohlcv-full-bar-data`

Same response structure as `tokens/ohlcv-full-bar-data` above.

### Token detail — `tokens/symbol`

Wrapper: `APIResponse` -- the `response` field contains an array of Token objects; `total` gives the count.

**Each item in `response` (Token):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Trade pair ID | `tradePairId` | integer | Internal trading pair identifier |
| Address | `address` | string | Token contract address |
| Chain type | `chainType` | integer | Blockchain type identifier (e.g. 1 = ETH) |
| Symbol | `symbol` | string | Token symbol (e.g. `"BTC"`) |
| Logo | `logo` | string | URL to the token logo image |
| Twitter URL | `twitterUrl` | string | Token Twitter/X profile URL |
| Website URL | `websiteUrl` | string | Token official website URL |
| Price change | `priceChange` | string | Price change ratio over the interval (e.g. `"0.033"` = 3.3%) |
| Open price | `openPrice` | string | Opening price (string for precision) |
| Close price | `closePrice` | string | Closing / current price (string for precision) |
| High price | `highPrice` | string | Highest price in the interval (string for precision) |
| Low price | `lowPrice` | string | Lowest price in the interval (string for precision) |
| Total volume | `totalVolume` | string | Total trading volume (string for precision) |

### Previous 24h close — `tokens/previous-24-hours-close-price`

Wrapper: `APIResponse` -- the `response` field contains the object below.

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Close price | `close_price` | number | The closing price from 24 hours before the given timestamp |

### Market cap — `tokens/market-cap`

Wrapper: `APIResponseV2` -- the `data` field is a flat array of market-cap items.

**Each item in `data` (TokenMarketCapItem):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Symbol | `symbol` | string | Token symbol |
| Name | `name` | string | Token name (may be omitted) |
| Timestamp | `timestamp` | integer | Unix timestamp in seconds |
| Time | `time` | string | Formatted time in RFC 3339 / ISO 8601 UTC |
| Market cap | `marketCap` | number | Market capitalization in USD |

### Supply — `tokens/supply`

Wrapper: `APIResponseV2` -- the `data` field is a flat array of supply items.

**Each item in `data` (TokenSupplyItem):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Symbol | `symbol` | string | Token symbol |
| Name | `name` | string | Token name (may be omitted) |
| Timestamp | `timestamp` | integer | Unix timestamp in seconds |
| Time | `time` | string | Formatted time in RFC 3339 / ISO 8601 UTC |
| Circulating supply | `circulatingSupply` | number | Current circulating supply |
| Total supply | `totalSupply` | number | Total supply |

### Stock kline — `stocks/kline`

Wrapper: `APIResponse` -- the `response` field contains the object below.

**Top-level response object:**

| Field | Type | Description |
|-------|------|-------------|
| `data` | array | Array of stock kline data items (see below) |
| `count` | integer | Number of data points returned |
| `cursor` | string | Pagination cursor for the next page; empty if no more data |

**Each item in `data` (StockKlineData):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Time open | `time_open` | integer | K-line open time (Unix timestamp, seconds, UTC) |
| Time close | `time_close` | integer | K-line close time (Unix timestamp, seconds, UTC) |
| Period start | `time_period_start` | string | Open time in RFC 3339 format (e.g. `"2024-07-24T00:00:00Z"`) |
| Period end | `time_period_end` | string | Close time in RFC 3339 format |
| Open price | `price_open` | number | Opening price |
| Close price | `price_close` | number | Closing price |
| Low price | `price_low` | number | Lowest price |
| High price | `price_high` | number | Highest price |
| Trades count | `trades_count` | integer | Number of trades |
| Volume traded | `volume_traded` | number | Total traded volume |

### Stock OHLCV full bar — `stocks/ohlcv-full-bar-data`

Wrapper: `APIResponseV2` -- the `data` field is a flat array of StockKlineData items.

**Response fields:** Same StockKlineData fields as `stocks/kline` above (no cursor, no wrapping object -- just the array directly in `data`).

### Stock previous 24h close — `stocks/previous-24-hours-close-price`

Same response structure as `tokens/previous-24-hours-close-price` above.

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Close price | `close_price` | number | The closing price from the previous trading day at the given timestamp |

### V2 stock kline — `v2/stocks/kline`

Wrapper: `APIResponseV2` -- the `data` field is a flat array of StockKlineData items.

**Response fields:** Same StockKlineData fields as `stocks/kline` above (no cursor, no wrapping object -- just the array directly in `data`).

## Calculating crypto volatility from kline data

To compute daily volatility for a crypto asset, fetch daily kline data over the desired lookback window, compute log returns between consecutive closes, then take the **population standard deviation (divide by N, not N-1)**.

**IMPORTANT**: For an "N-day window ending on date D", fetch N+1 candles ending on date D (you need N+1 prices to get N log returns). Set `end_time` to the target date (NOT the next day) to ensure the target date is the last candle.

```python
import requests, os, math, calendar
from datetime import datetime, timezone, timedelta

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

def to_ts(year, month, day, hour=0):
    return int(calendar.timegm(datetime(year, month, day, hour, tzinfo=timezone.utc).timetuple()))

# Daily volatility of BTC on Aug 9, 2025 with 30-day window
target = datetime(2025, 8, 9, tzinfo=timezone.utc)
lookback_start = target - timedelta(days=30)  # Jul 10
start = to_ts(lookback_start.year, lookback_start.month, lookback_start.day)
end = to_ts(2025, 8, 9)  # target date itself (NOT next day)

resp = requests.get(f"{base}/api/v1/tokens/kline",
    params={"symbol": "BTC", "start_time": start, "end_time": end,
            "interval": "1d", "limit": 35},
    headers={"X-API-Key": key})
body = resp.json()
candles = body["response"]["data"]
candles.sort(key=lambda x: x["time_open"])
closes = [c["price_close"] for c in candles]
log_returns = [math.log(closes[i] / closes[i-1]) for i in range(1, len(closes))]
n = len(log_returns)
mean_r = sum(log_returns) / n
variance = sum((r - mean_r) ** 2 for r in log_returns) / n  # population variance (N)
daily_vol = math.sqrt(variance)
print(f"{daily_vol * 100:.2f}%")
```

## Python examples

```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# Crypto kline (APIResponse — data in body["response"]["data"])
resp = requests.get(f"{base}/api/v1/tokens/kline",
    params={"symbol": "ETH", "start_time": 1723420800, "end_time": 1723507200,
            "interval": "1d", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
candles = body["response"]["data"]  # response > data array
for c in candles:
    print(f"Open: {c['price_open']}, Close: {c['price_close']}")

# Crypto OHLCV full bar (APIResponseV2 — data in body["data"])
resp = requests.get(f"{base}/api/v1/tokens/ohlcv-full-bar-data",
    params={"symbol": "BTC", "start_time": 1723420800, "end_time": 1723507200,
            "interval": "1d", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
bars = body["data"]  # flat array directly

# Stock kline (APIResponse — data in body["response"]["data"])
resp = requests.get(f"{base}/api/v1/stocks/kline",
    params={"ticker": "AAPL", "start_time": 1724630400, "end_time": 1724716800,
            "interval": "1d", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
candles = body["response"]["data"]  # response > data array
for c in candles:
    print(f"Close: {c['price_close']}")

# Market cap (APIResponseV2 — data in body["data"])
resp = requests.get(f"{base}/api/v1/tokens/market-cap",
    params={"symbol": "BTC", "start_time": 1723420800, "end_time": 1723507200},
    headers={"X-API-Key": key})
body = resp.json()
for item in body["data"]:  # flat array
    print(f"Market Cap: ${item['marketCap']:,.0f}")

# Token supply (APIResponseV2 — data in body["data"])
resp = requests.get(f"{base}/api/v1/tokens/supply",
    params={"symbol": "BTC", "start_time": 1723420800, "end_time": 1723507200},
    headers={"X-API-Key": key})
body = resp.json()
for item in body["data"]:  # flat array
    print(f"Circulating: {item['circulatingSupply']}, Total: {item['totalSupply']}")

# Futures trading volume — use futures/ohlcv-full-bar-data (APIResponseV2)
# volume_traded is already in quote currency (USDT), no price conversion needed
import calendar
from datetime import datetime, timezone
def to_ts(y, m, d):
    return int(calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple()))

resp = requests.get(f"{base}/api/v1/tokens/futures/ohlcv-full-bar-data",
    params={"symbol": "ETHUSDT", "start_time": to_ts(2025, 9, 6),
            "end_time": to_ts(2025, 9, 7), "interval": "1d", "limit": 5},
    headers={"X-API-Key": key})
body = resp.json()
for bar in body["data"]:
    if "2025-09-06" in bar.get("time_period_start", ""):
        print(f"Futures volume: ${bar['volume_traded']:,.2f}")  # already in USDT
```

## Price Correlation Between Two Assets

To compute the correlation between two assets (e.g., BTC and TLT), use **Pearson correlation of closing price levels** (NOT returns). Fetch kline data for both, align on common dates, then compute correlation.

**Steps**: (1) Fetch both klines, (2) Build date→close maps, (3) Align on common dates only (stocks/ETFs have no weekend data), (4) Compute Pearson correlation of price levels.

```python
# Pearson correlation of price levels (NOT returns)
btc_prices = {c["time_period_start"][:10]: c["price_close"] for c in btc_kline}
tlt_prices = {c["time_period_start"][:10]: c["price_close"] for c in tlt_kline}
common = sorted(set(btc_prices) & set(tlt_prices))
bv = [btc_prices[d] for d in common]
tv = [tlt_prices[d] for d in common]
n = len(bv)
mb, mt = sum(bv)/n, sum(tv)/n
cov = sum((bv[i]-mb)*(tv[i]-mt) for i in range(n))/n
sb = (sum((x-mb)**2 for x in bv)/n)**0.5
st = (sum((x-mt)**2 for x in tv)/n)**0.5
print(f"{cov/(sb*st):.4f}")
```
