---
name: arrays-data-api-spot-market-price-and-volume
description: Calls Arrays REST APIs for spot market prices and volume — stock and crypto price/volume/candlestick/kline/OHLCV data, token details, and previous close. Use when the user asks for raw price/volume/OHLCV/candlestick/kline data. For metrics including market cap, crypto supply, moving averages, EMA, SMA, RSI, MACD, Bollinger Bands, VWAP, beta, volatility, PE ratio, PB ratio, PS ratio, dividend yield, enterprise value, EV/EBITDA, price change percentages (1d/1w/1M/3M/6M/YTD/1Y), use arrays-data-api-stock-metrics for stocks and arrays-data-api-crypto-metrics-and-screener for crypto.
---


# Arrays Data API — Spot Market Price and Volume

Stock and crypto kline/OHLCV, token detail by symbol, previous close, and full bar data.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- **Data ordering**: Kline results are returned in **reverse chronological order** (latest first). Always match by `time_period_start` to get a specific date, or use `data[0]` to get the most recent data point.
- **Timestamp Rule**: Date fields are stored in UTC for crypto data and US Eastern time (ET) for US stocks. To include a full day's data, set `end_time` to midnight of the **next** day — e.g. for US stock data on 2024-12-31: `end_time = int(datetime(2025, 1, 1, 0, 0, 0, tzinfo=ET).timestamp())`; for crypto on 2024-12-31: `end_time = int(datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc).timestamp())`

## Crypto — `/api/v1/crypto/`

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `detail` | `crypto-detail` | Token detail by symbol |
| GET | `kline` | `crypto-kline` | Crypto kline (candlestick) data (use this for BTC, ETH price queries) |
| GET | `ohlcv` | `crypto-ohlcv` | Crypto OHLCV full bar data (requires specific trading pair) |
| GET | `futures/ohlcv` | `crypto-futures-ohlcv` | Crypto futures OHLCV data — use this for "futures trading volume" queries. `volume_traded` is in **quote currency (USDT)**, no conversion needed. Symbol format: `ETHUSDT`, `BTCUSDT` |

### Stocks — `/api/v1/stocks/`

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `kline` | `stocks-kline` | Stock kline (candlestick) data |

## Parameters by endpoint

### Kline endpoints (`crypto/kline`, `stocks/kline`, `crypto/ohlcv`, etc.)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (e.g. `BTC`, `ETH`) or stock symbol (e.g. `AAPL`, `TSLA`) |
| `start_time` | int | yes | Start time (Unix seconds). Must be > 0 |
| `end_time` | int | yes | End time (Unix seconds). Must be > start_time |
| `interval` | string | yes | Time interval: `1min`, `2min`, `3min`, `5min`, `10min`, `15min`, `30min`, `45min`, `1h`, `2h`, `4h`, `1d`, `1w`, `1m`, `3m`, `6m` |
| `limit` | int | no | Max data points. Default 500, max 10000 |
| `cursor` | string | no | Pagination cursor (only for `crypto/kline`) |

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `crypto/detail` | `crypto-detail` | Token detail |
| GET | `crypto/kline` | `crypto-kline` | Crypto kline |
| GET | `crypto/ohlcv` | `crypto-ohlcv` | Crypto OHLCV full bar |
| GET | `crypto/futures/ohlcv` | `crypto-futures-ohlcv` | Crypto futures OHLCV full bar |
| GET | `stocks/kline` | `stocks-kline` | Stock kline |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


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

resp = requests.get(f"{base}/api/v1/crypto/kline",
    params={"symbol": "BTC", "start_time": start, "end_time": end,
            "interval": "1d", "limit": 35},
    headers={"X-API-Key": key})
body = resp.json()
candles = body["data"]
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

# Crypto kline
resp = requests.get(f"{base}/api/v1/crypto/kline",
    params={"symbol": "ETH", "start_time": 1723420800, "end_time": 1723507200,
            "interval": "1d", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
candles = body["data"]  # data array
for c in candles:
    print(f"Open: {c['price_open']}, Close: {c['price_close']}")

# Crypto OHLCV full bar
resp = requests.get(f"{base}/api/v1/crypto/ohlcv",
    params={"symbol": "BTC", "start_time": 1723420800, "end_time": 1723507200,
            "interval": "1d", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
bars = body["data"]  # data array

# Stock kline — end_time must be midnight ET of the NEXT day
from datetime import datetime, timezone, timedelta
ET = timezone(timedelta(hours=-5))  # or use ZoneInfo("America/New_York")
start_time = int(datetime(2024, 8, 26, 0, 0, 0, tzinfo=ET).timestamp())
end_time = int(datetime(2024, 8, 27, 0, 0, 0, tzinfo=ET).timestamp())  # next day midnight
resp = requests.get(f"{base}/api/v1/stocks/kline",
    params={"symbol": "AAPL", "start_time": start_time, "end_time": end_time,
            "interval": "1d", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
candles = body["data"]  # data array
for c in candles:
    print(f"Close: {c['price_close']}")

# Futures trading volume — use futures/ohlcv
# volume_traded is already in quote currency (USDT), no price conversion needed
import calendar
from datetime import datetime, timezone
def to_ts(y, m, d):
    return int(calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple()))

resp = requests.get(f"{base}/api/v1/crypto/futures/ohlcv",
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
