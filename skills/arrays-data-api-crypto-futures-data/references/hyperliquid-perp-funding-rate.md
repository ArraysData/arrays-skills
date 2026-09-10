# Hyperliquid perpetual funding rate

`GET /api/v1/crypto/hyperliquid/perp/funding-rate`

Hourly funding rate history for a Hyperliquid perpetual — native crypto perps and HIP-3 listings alike. Settles every hour on the hour (UTC). Coverage from 2023-05 for the original perps; HIP-3 listings start at their listing date.

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Hyperliquid canonical base symbol, case-insensitive (`BTC`, `ETH`, `HYPE`; HIP-3: `NVDA`, `AAPL`, `TSLA`). Same symbol guide as `hyperliquid-perp-usdc-kline`. Unknown symbol → `400 INVALID_PARAMETER` |
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds) |
| `limit` | int32 | no | Max results (1–1000, default 100) |
| `sort_order` | string | no | `asc` or `desc` (default `desc`, newest first) |

Response envelope: `{ "success": true, "request_id": "...", "data": [ ... ] }`

**Each item in `data`:**

| Field | Type | Description |
|-------|------|-------------|
| `funding_rate` | float64 | Hourly funding rate as a decimal (`0.0000125` = 0.00125 %). Positive means longs pay shorts. For a historical eight-hour comparison, sum all eight hourly rates over the same settlement window; verify that all eight observations are present. Multiplying one hourly rate by 8 is only an estimate assuming the rate stays constant |
| `timestamp` | int64 | Settlement instant (Unix seconds, UTC, on the hour) |

```json
{ "success": true, "data": [ { "funding_rate": 1.25e-05, "timestamp": 1788940800 } ], "request_id": "..." }
```
