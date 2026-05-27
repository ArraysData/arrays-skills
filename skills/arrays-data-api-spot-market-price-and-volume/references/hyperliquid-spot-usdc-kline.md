# Hyperliquid spot USDC kline

`GET /api/v1/crypto/hyperliquid/spot/usdc/kline`

**Timestamp Rule**: query window is in UTC Unix seconds. Bar boundaries align to UTC (00:00 UTC for `1d`+). A bar is only returned once fully closed and only if the query range fully contains `[time_open, time_close]`. The quote currency is fixed at USDC in the URL path — pass only the base token symbol (`HYPE`, `BTC`).

**Symbol guide** — HL spot has two distinct deployment lanes:

| Token class | Symbol | Note |
|---|---|---|
| Unit-bridged tokens (require `U-` prefix) | `UBTC`, `UETH`, `USOL`, `UZEC`, `UBONK`, `UFART`, `UPUMP`, `UENA`, `UXPL`, `UMON`, `UAVAX`, etc. | `BTC` / `ETH` / `SOL` / `ZEC` also accept the naked form as legacy alias |
| HL ecosystem HIP-2 tokens (no prefix) | `HYPE`, `HFUN`, `PEPE`, `ZAMA`, `SIGN`, etc. | Independent native HL deployments |

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | See Symbol guide above |
| `start_time` | integer | yes | Start time (Unix seconds). Must be > 0 |
| `end_time` | integer | yes | End time (Unix seconds). Must be > start_time |
| `interval` | string | yes | `1min`, `5min`, `15min`, `30min`, `1h`, `4h`, `1d`, `1w`, `1m` |
| `limit` | integer | no | Max data points. Default 500, max 10000 |

Response envelope: `{ "success": true, "data": [ ... ], "request_id": "..." }` — `data` is an array of candle items, in **reverse chronological order** (latest first).

**Each item in `data`:**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Time open | `time_open` | string | Bar open time, RFC 3339 (e.g. `"2025-11-05T00:00:00Z"`) |
| Time close | `time_close` | string | Bar close time, RFC 3339 |
| Open price | `price_open` | number | Opening price (USDC) |
| High price | `price_high` | number | Highest price in the interval (USDC) |
| Low price | `price_low` | number | Lowest price in the interval (USDC) |
| Close price | `price_close` | number | Closing price (USDC) |
| Volume | `volume` | number | Trading volume in **base-asset units** (multiply by price for USDC notional) |
