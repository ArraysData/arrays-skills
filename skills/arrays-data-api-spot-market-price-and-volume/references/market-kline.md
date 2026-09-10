# Unified market kline

`GET /api/v1/market/kline`

One OHLCV shape for any listed instrument, addressed by `trading_pair`. Newest first.

**`trading_pair` format**: `<MARKET>_<TYPE>_<SYMBOL>_<QUOTE>`, all upper case. Supported types are `SPOT`, `PERP`, `OPTION`, and `FUTURE`, in the combinations below. ETFs use `US_SPOT` (for example, `US_SPOT_SPY_USD`); `US_ETF` is not supported. Discover a symbol's pairs with `market/trading-pairs`.

| Asset | `trading_pair` example | Intervals |
|-------|------------------------|-----------|
| Crypto spot (Binance) | `BINANCE_SPOT_BTC_USDT` | all |
| Crypto perp (Binance) | `BINANCE_PERP_ETH_USDT` | all |
| Hyperliquid spot | `HYPERLIQUID_SPOT_HYPE_USDC` | all |
| Hyperliquid perp, incl. HIP-3 | `HYPERLIQUID_PERP_NVDA_USDC` | all |
| US stock | `US_SPOT_AAPL_USD` | all; `1d`+ needs `session=RTH` |
| US ETF | `US_SPOT_SPY_USD` | all; `1d`+ needs `session=RTH` |
| US stock / ETF / index option | `US_OPTION_AAPL260918C00230000_USD` | all |
| US index | `US_SPOT_SPX_USD` | `1d` only |
| CME commodity future | `CME_FUTURE_GCUSD_USD` | `1d` only |
| FX spot | `FX_SPOT_EURUSD_USD` | `1d` only |

Non-US dotted symbols (`0700.HK`) are rejected; use `stocks/non-us/kline`. An unsupported interval for the asset class, or an unknown symbol, returns `400` with the supported set in the message.

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `trading_pair` | string | yes | See format above |
| `start_time` | string | yes | RFC 3339 / ISO 8601 (`2026-09-01T00:00:00Z`). Unix seconds are rejected |
| `end_time` | string | yes | RFC 3339 / ISO 8601 |
| `interval` | string | yes | `1min`, `5min`, `15min`, `30min`, `1h`, `4h`, `1d`, `1w`, `1m` (`1m` = one month) |
| `limit` | int | no | Max bars for crypto spot/perps and US stocks, ETFs and options (default 500, max 10000). Ignored for indices, CME commodity futures and FX; narrow the time window to bound those responses |
| `session` | string | no | `RTH` or `ETH` (default `ETH`); stocks, ETFs and options only. **Pass `RTH` for US stocks and ETFs at `1d`, `1w`, `1m`** |

Response envelope: `{ "success": true, "request_id": "...", "count": 64, "data": [ ... ] }` — `count` is the number of bars returned.

**Each item in `data`:**

| Field | Type | Description |
|-------|------|-------------|
| `time_open` | string | Bar open, RFC 3339 UTC |
| `time_close` | string | Bar close, RFC 3339 UTC |
| `price_open` | float64 | Open |
| `price_high` | float64 | High |
| `price_low` | float64 | Low |
| `price_close` | float64 | Close |
| `volume` | float64 | Volume in base-asset units (shares, contracts, coins) |

```python
import os, requests
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# Daily bars for a US stock: RFC 3339 times and session=RTH
resp = requests.get(f"{base}/api/v1/market/kline",
    params={"trading_pair": "US_SPOT_AAPL_USD", "interval": "1d", "session": "RTH",
            "start_time": "2026-09-01T00:00:00Z", "end_time": "2026-09-08T00:00:00Z"},
    headers={"X-API-Key": key})
for bar in resp.json()["data"]:  # newest first
    print(bar["time_open"], bar["price_close"])
```
