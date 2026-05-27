# Hyperliquid perpetual USDC kline

`GET /api/v1/crypto/hyperliquid/perp/usdc/kline`

**Timestamp Rule**: query window is in UTC Unix seconds. Bar boundaries align to UTC (00:00 UTC for `1d`+). A bar is only returned once fully closed and only if the query range fully contains `[time_open, time_close]`. The quote currency is fixed at USDC in the URL path — pass the HL canonical symbol per the table below. For funding rate / open interest see the other endpoints in this skill.

**Symbol guide** — HL HIP-3 covers many asset classes beyond crypto. Use HL's canonical name, **not** the popular US ticker:

| Asset class | HL canonical symbol | Common ticker that does NOT work |
|---|---|---|
| Native crypto perps | `BTC`, `ETH`, `SOL`, `HYPE`, `DOGE`, `XRP`, `BNB`, `AVAX`, `LINK`, etc. (US ticker) | — |
| Single stocks (HIP-3) | `NVDA`, `AAPL`, `TSLA`, `HOOD`, `GOOGL`, `MSFT`, `AMZN`, `META`, `INTC`, `ORCL`, etc. (US ticker) | `GOOG` → use `GOOGL` |
| Stock indices | `SP500`, `XYZ100`, `JP225`, `KR200` | `SPY/VOO/IVV/SPX` (SPX is memecoin), `QQQ/NDX/USA100`, `NIKKEI`, `KOSPI` |
| Commodities | `GOLD`, `SILVER`, `BRENTOIL`, `NATGAS`, `PLATINUM`, `PALLADIUM`, `COPPER` | `GLD/IAU`, `SLV`, `BNO`, `UNG`, `PPLT`, `PALL`, `CPER` |
| FX pairs | `EUR`, `JPY` | `FXE/EURUSD`, `FXY/USDJPY` |
| Some sector / country ETFs | `EWJ`, `EWY`, `URNM`, `XLE`, `DRAM`, `EWZ` (US ticker preserved) | — |

Full canonical symbol list for HIP-3 non-crypto assets: [xyz dex specification index](https://docs.trade.xyz/consolidated-resources/specification-index) (xyz is the largest HIP-3 deployer covering indices / commodities / FX / ETFs / equities on HL perp).

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
| Open price | `price_open` | number | Opening mark price (USDC) |
| High price | `price_high` | number | Highest price in the interval (USDC) |
| Low price | `price_low` | number | Lowest price in the interval (USDC) |
| Close price | `price_close` | number | Closing mark price (USDC) |
| Volume | `volume` | number | Trading volume in **base-asset units** (multiply by price for USDC notional) |
