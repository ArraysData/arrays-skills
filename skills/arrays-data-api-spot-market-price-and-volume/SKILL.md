---
name: arrays-data-api-spot-market-price-and-volume
description: Calls Arrays REST APIs for spot market prices and volume — US and non-US stock kline plus crypto spot price/volume/candlestick/kline/OHLCV data on Binance (spot USDT) and Hyperliquid (spot USDC). Also the unified `market/kline` endpoint, which returns the same OHLCV shape for any listed instrument by `trading_pair` — crypto spot and perps (Binance, Hyperliquid incl. HIP-3), US stocks, ETFs and options, US indices, CME commodity futures and FX — plus `market/trading-pairs` to discover the venues a symbol trades on. Use when the user asks for raw spot price/volume/OHLCV/candlestick/kline data, Binance or Hyperliquid spot prices, HYPE candles, non-US stock kline (daily or intraday) for dotted-suffix tickers like `0700.HK`, `9988.HK`, or `000660.KS`, one kline call across asset classes, or which markets a symbol is listed on. For perpetual futures kline / volume / funding rate / open interest / long-short ratio / taker buy-sell volume / HIP-3 tokenized equities (AAPL, TSLA on Hyperliquid), use arrays-data-api-crypto-futures-data. For token metadata profile (name, category, description, logo, contracts, official URLs) and metrics including market cap, crypto supply, moving averages, EMA, SMA, RSI, MACD, Bollinger Bands, VWAP, beta, volatility, PE ratio, PB ratio, PS ratio, dividend yield, enterprise value, EV/EBITDA, price change percentages (1d/1w/1M/3M/6M/YTD/1Y), use arrays-data-api-stock-metrics for stocks and arrays-data-api-crypto-metrics-and-screener for crypto.
---


# Arrays Data API — Spot Market Price and Volume

US and non-US stock kline plus crypto spot kline/OHLCV (Binance USDT, Hyperliquid USDC), and the unified `market/kline` for any instrument by `trading_pair`. For token metadata profile by symbol (`crypto/detail`), use arrays-data-api-crypto-metrics-and-screener.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.arrays.org`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- **Data ordering**: All kline endpoints return **reverse chronological** (latest first; use `data[0]` or match by timestamp). `stocks/kline` uses `time_period_start`; new crypto endpoints use `time_open`.
- **Non-US stocks**: `stocks/non-us/kline` supports intervals `1min` `5min` `15min` `30min` `1h` `4h` `1d` `1w` `1m` (intraday rolled up from 1-minute bars), uses dotted-suffix symbols (`0700.HK`, `9988.HK`, `000660.KS`), and prices come back in **local currency** (tagged per-bar via `quote_currency`: `HKD`, `JPY`, `GBp`, …). **Minor-unit venues (`*.L` pence, `*.TA` agorot, `*.JO` cents) return prices in sub-units — divide by 100 for GBP/ILS/ZAR.** Bar UTC times track the local exchange session (HKEX morning open is 01:30 UTC, etc.), so bars are not midnight-aligned. **Coverage is a curated subset, not every non-US listing** — only a selected list of symbols is backed by data (currently spanning exchanges such as HKEX `.HK`, KRX `.KS`, SIX `.SW`; many exchanges/tickers are not yet included).
- **`volume` unit**: All endpoints return `volume` in **base-asset units** (BTC, ETH, HYPE, shares, etc.) — multiply by a representative bar price for notional. `stocks/kline` uses the legacy field name `volume_traded`.
- **Quote currency scope**: Binance only via **USDT** pairs; Hyperliquid only via **USDC** pairs. Other quote currencies (Binance `USDC/FDUSD/BTC`, Hyperliquid HIP-3 `USDH/USDE/USDT` etc.) are not exposed by these endpoints.
- **Timestamp Rule**: Date fields are stored in UTC for crypto data and US Eastern time (ET) for US stocks. A bar is only returned if the query range fully contains `[time_open, time_close]`.
- **Bar boundaries**: Stock intraday RTH: 9:30–16:00 ET; intraday ETH: 4:00–20:00 ET. `1d`: 9:30–16:00 ET (RTH only). `1w`/`1m`/`3m`: midnight ET. Crypto: midnight UTC.
- **Session filter**: `session=ETH` is only valid for intraday intervals. Using it with `1d` or higher returns an error.
- **Unified `market/kline`**: one call shape for every asset class, but a different contract from the endpoints above — `trading_pair` instead of `symbol`, **RFC 3339** `start_time` / `end_time` instead of Unix seconds, and a fixed interval set (`1min` `5min` `15min` `30min` `1h` `4h` `1d` `1w` `1m`). **US stocks and ETFs at `1d` or above require `session=RTH`.** Indices, CME futures and FX are daily only. Non-US dotted symbols are not accepted — use `stocks/non-us/kline`. Prefer the dedicated endpoints when one exists for the asset; reach for `market/kline` when you need perps, options, futures, FX or indices, or one loop over mixed assets.

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `/api/v1/crypto/binance/spot/usdt/kline` | `binance-spot-usdt-kline` | Binance spot USDT kline (use as default for BTC, ETH, etc., or when no exchange is named)  |
| GET | `/api/v1/crypto/hyperliquid/spot/usdc/kline` | `hyperliquid-spot-usdc-kline` | Hyperliquid spot USDC kline (use for HYPE, or when the user explicitly says "on Hyperliquid")|
| GET | `/api/v1/stocks/kline` | `stocks-kline` | US stock kline |
| GET | `/api/v1/stocks/non-us/kline` | `stocks-non-us-kline` | Non-US stock kline (`1min`–`1m`; dotted-suffix symbols like `0700.HK`; local-currency prices, minor-unit venues in sub-units) |
| GET | `/api/v1/market/kline` | `market-kline` | Unified OHLCV by `trading_pair` (`BINANCE_SPOT_BTC_USDT`, `US_SPOT_AAPL_USD`, `HYPERLIQUID_PERP_NVDA_USDC`, `US_OPTION_…`, `CME_FUTURE_GCUSD_USD`, `FX_SPOT_EURUSD_USD`); RFC 3339 times |
| GET | `/api/v1/market/trading-pairs` | `market-trading-pairs` | Every `trading_pair` a symbol trades as, grouped by instrument type |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.

## Parameters by endpoint

### Kline endpoints (`crypto/binance/spot/usdt/kline`, `crypto/hyperliquid/spot/usdc/kline`, `stocks/kline`, `stocks/non-us/kline`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Base token (e.g. `BTC`, `ETH`, `HYPE`) for crypto — never `BTCUSDT`, the quote currency is fixed in the URL path. US stock symbol (e.g. `AAPL`, `TSLA`) for `stocks/kline`. Non-US dotted-suffix symbol (e.g. `0700.HK`, `000660.KS`) for `stocks/non-us/kline`. |
| `start_time` | int | yes | Start time (Unix seconds). Must be > 0 |
| `end_time` | int | yes | End time (Unix seconds). Must be > start_time |
| `interval` | string | yes | `1min`, `2min`, `3min`, `5min`, `10min`, `15min`, `30min`, `45min`, `1h`, `2h`, `4h`, `1d`, `1w`, `1m`, `3m`, `6m` (Binance + `stocks/kline`). Hyperliquid and `stocks/non-us/kline` are narrower: `1min`, `5min`, `15min`, `30min`, `1h`, `4h`, `1d`, `1w`, `1m`. |
| `limit` | int | no | Max data points. Default 500, max 10000. |


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

# US Stock kline — end_time must be midnight ET of the NEXT day
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

# Non-US stock kline — dotted symbol, 1min–1m intervals, latest-first,
# prices in quote_currency (HKD, JPY, GBp/pence for .L, …)
resp = requests.get(f"{base}/api/v1/stocks/non-us/kline",
    params={"symbol": "0700.HK", "start_time": 1748563200, "end_time": 1748908800,
            "interval": "1d", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
bars = body["data"]  # latest first
latest = bars[0]
print(f"{latest['time_period_end']}: close={latest['price_close']} {latest['quote_currency']}, "
      f"vol={latest['volume_traded']:.0f}")

# Convert a local-currency close to USD (single bar).
# Non-US kline prices are in quote_currency (HKD, JPY, GBp for .L, …), NOT USD. Pull the
# matching <CCY>USD daily series from /api/v1/macro/forex/historical and use the FX
# `close` for the SAME calendar date as the stock bar. If that date has no FX bar
# (FX holiday/weekend), fall back to the next available FX close.
ccy = latest["quote_currency"]             # e.g. "HKD"
bar_date = latest["time_period_end"][:10]  # ISO date of the stock bar, e.g. "2025-05-30"
resp = requests.get(f"{base}/api/v1/macro/forex/historical",
    params={"symbol": f"{ccy}USD", "start_time": 1748563200, "end_time": 1748908800,
            "limit": 10},
    headers={"X-API-Key": key})
fx = {row["date"]: row["close"] for row in resp.json()["data"]}  # date -> CCY->USD close
rate = fx.get(bar_date) or fx[min(d for d in fx if d >= bar_date)]  # same date, else next
print(f"close in USD: {latest['price_close'] * rate:.2f} (rate {ccy}USD={rate} on {bar_date})")
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
