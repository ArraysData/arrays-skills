---
name: arrays-data-api-spot-market-price-and-volume
description: Calls Arrays REST APIs for spot market prices and volume — stock and crypto spot price/volume/candlestick/kline/OHLCV data on Binance (spot USDT) and Hyperliquid (spot USDC), and token detail metadata. Use when the user asks for raw spot price/volume/OHLCV/candlestick/kline data, Binance or Hyperliquid spot prices, or HYPE candles. For perpetual futures kline / volume / funding rate / open interest / long-short ratio / taker buy-sell volume / HIP-3 tokenized equities (AAPL, TSLA on Hyperliquid), use arrays-data-api-crypto-futures-data. For metrics including market cap, crypto supply, moving averages, EMA, SMA, RSI, MACD, Bollinger Bands, VWAP, beta, volatility, PE ratio, PB ratio, PS ratio, dividend yield, enterprise value, EV/EBITDA, price change percentages (1d/1w/1M/3M/6M/YTD/1Y), use arrays-data-api-stock-metrics for stocks and arrays-data-api-crypto-metrics-and-screener for crypto.
---


# Arrays Data API — Spot Market Price and Volume

Stock and crypto spot kline/OHLCV (Binance USDT, Hyperliquid USDC) and token detail by symbol.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- **Data ordering**: All kline endpoints return **reverse chronological** (latest first; use `data[0]` or match by timestamp). `stocks/kline` uses `time_period_start`; new crypto endpoints use `time_open`.
- **`volume` unit**: All endpoints return `volume` in **base-asset units** (BTC, ETH, HYPE, shares, etc.) — multiply by a representative bar price for notional. `stocks/kline` uses the legacy field name `volume_traded`.
- **Quote currency scope**: Binance only via **USDT** pairs; Hyperliquid only via **USDC** pairs. Other quote currencies (Binance `USDC/FDUSD/BTC`, Hyperliquid HIP-3 `USDH/USDE/USDT` etc.) are not exposed by these endpoints.
- **Timestamp Rule**: Date fields are stored in UTC for crypto data and US Eastern time (ET) for US stocks. A bar is only returned if the query range fully contains `[time_open, time_close]`.
- **Bar boundaries**: Stock intraday RTH: 9:30–16:00 ET; intraday ETH: 4:00–20:00 ET. `1d`: 9:30–16:00 ET (RTH only). `1w`/`1m`/`3m`: midnight ET. Crypto: midnight UTC.
- **Session filter**: `session=ETH` is only valid for intraday intervals. Using it with `1d` or higher returns an error.

## Crypto — `/api/v1/crypto/`

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `detail` | `crypto-detail` | Token detail by symbol |
| GET | `binance/spot/usdt/kline` | `binance-spot-usdt-kline` | Binance spot USDT kline (default for BTC, ETH, etc. when no exchange is named) |
| GET | `hyperliquid/spot/usdc/kline` | `hyperliquid-spot-usdc-kline` | Hyperliquid spot USDC kline (use for HYPE, or when the user explicitly says "on Hyperliquid") |

### Stocks — `/api/v1/stocks/`

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `kline` | `stocks-kline` | Stock kline (candlestick) data |

## Parameters by endpoint

### Kline endpoints (`crypto/binance/spot/usdt/kline`, `crypto/hyperliquid/spot/usdc/kline`, `stocks/kline`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Base token (e.g. `BTC`, `ETH`, `HYPE`) for crypto — never `BTCUSDT`, the quote currency is fixed in the URL path. Stock symbol (e.g. `AAPL`, `TSLA`) for `stocks/kline`. |
| `start_time` | int | yes | Start time (Unix seconds). Must be > 0 |
| `end_time` | int | yes | End time (Unix seconds). Must be > start_time |
| `interval` | string | yes | `1min`, `2min`, `3min`, `5min`, `10min`, `15min`, `30min`, `45min`, `1h`, `2h`, `4h`, `1d`, `1w`, `1m`, `3m`, `6m` (Binance + stocks). Hyperliquid is narrower: `1min`, `5min`, `15min`, `30min`, `1h`, `4h`, `1d`, `1w`, `1m`. |
| `limit` | int | no | Max data points. Default 500, max 10000 |

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `crypto/detail` | `crypto-detail` | Token detail |
| GET | `crypto/binance/spot/usdt/kline` | `binance-spot-usdt-kline` | Binance spot USDT kline |
| GET | `crypto/hyperliquid/spot/usdc/kline` | `hyperliquid-spot-usdc-kline` | Hyperliquid spot USDC kline |
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

resp = requests.get(f"{base}/api/v1/crypto/binance/spot/usdt/kline",
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

# Binance spot kline (use for BTC, ETH, etc. when no exchange is named)
resp = requests.get(f"{base}/api/v1/crypto/binance/spot/usdt/kline",
    params={"symbol": "ETH", "start_time": 1723420800, "end_time": 1723507200,
            "interval": "1d", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
candles = body["data"]  # latest first
for c in candles:
    print(f"Open: {c['price_open']}, Close: {c['price_close']}")

# Hyperliquid spot kline — note volume is in base-asset (HYPE), not USDC
resp = requests.get(f"{base}/api/v1/crypto/hyperliquid/spot/usdc/kline",
    params={"symbol": "HYPE", "start_time": 1762300800, "end_time": 1762560000,
            "interval": "1d", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
for c in body["data"]:  # latest first
    notional_usdc = c["volume"] * (c["price_open"] + c["price_close"]) / 2
    print(f"Close: {c['price_close']}, vol_HYPE: {c['volume']}, ~vol_USDC: {notional_usdc:.0f}")

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
```

## Price Correlation Between Two Assets

To compute the correlation between two assets (e.g., BTC and TLT), use **Pearson correlation of closing price levels** (NOT returns). Fetch kline data for both, align on common dates, then compute correlation.

**Steps**: (1) Fetch both klines, (2) Build date→close maps, (3) Align on common dates only (stocks/ETFs have no weekend data), (4) Compute Pearson correlation of price levels.

```python
# Pearson correlation of price levels (NOT returns)
# Crypto kline returns time_open as RFC 3339 string; stocks/kline still uses time_period_start
btc_prices = {c["time_open"][:10]: c["price_close"] for c in btc_kline}
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
