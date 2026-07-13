# Non-US stock daily kline (OHLCV)

`GET /api/v1/stocks/non-us/kline`

Split-adjusted **daily** bars for non-US tickers in dotted form (e.g. `0700.HK`, `9988.HK`, `000660.KS`). Only the `1d` interval is supported.

> **Coverage is a curated subset.** Only a selected list of non-US symbols is currently supported (spanning exchanges such as HKEX `.HK`, KRX `.KS`, SIX `.SW`; many exchanges and tickers are not yet included). Don't assume an arbitrary dotted ticker resolves. Bars are returned in **reverse chronological** order (latest first; use `data[0]` for the most recent), matching the other kline endpoints in this skill. Timestamps are UTC but bar boundaries follow the local exchange session (HKEX morning open is 01:30 UTC, etc.), so a daily bar's UTC times are not midnight-aligned.

> **⚠️ Prices are in local currency, NOT USD.** Every bar carries a `quote_currency` field (`HKD` for `*.HK`, `JPY` for `*.T`, `GBP` for `*.L`, etc.). Always read `quote_currency` from the response — never assume the price column is in USD or use it as a USD value without first converting via an FX rate. Display the currency alongside any price you surface to the user.

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Non-US ticker in `<TICKER>.<EXCHANGE_SUFFIX>` form (e.g. `0700.HK`, `000660.KS`). The suffix is part of the symbol — passing the bare ticker (`0700`) will not resolve. |
| `start_time` | int | yes | Start time (Unix seconds). Must be > 0 |
| `end_time` | int | yes | End time (Unix seconds). Must be > `start_time` |
| `interval` | string | no | Bar size. Only `1d` is supported (default `1d`). Intraday intervals are not available for this endpoint. |
| `limit` | int | no | Max bars. Default 500, max 10000 |

## Response

**Each item in the `data` array (one bar):**

| Field | Type | Description |
|-------|------|-------------|
| `price_open` | number | Opening price (in `quote_currency`) |
| `price_high` | number | Session high |
| `price_low` | number | Session low |
| `price_close` | number | Closing price |
| `volume_traded` | number | Volume in shares (base asset) |
| `time_open` | int | Bar open time (Unix seconds, UTC) |
| `time_close` | int | Bar close time (Unix seconds, UTC) |
| `time_period_start` | string | Bar open time in RFC 3339 (e.g. `"2025-05-30T01:30:00Z"`) |
| `time_period_end` | string | Bar close time in RFC 3339 |
| `quote_currency` | string | Currency of the price fields — `HKD` (`*.HK`), `JPY` (`*.T`), `GBP` (`*.L`), etc. **Always read this**; prices are in local currency, never USD. |

The response envelope also includes `pagination: { limit, offset }` and `request_id`.

---
