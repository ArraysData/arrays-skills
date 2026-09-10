# 4. Real-time data

`GET /api/v1/macro/index/real-time`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Symbol identifier |

**Response** — `data` is an array:
```json
{ "success": true, "request_id": "...", "data": [ { "symbol": "^SPX", "date": "2026-01-15T14:26:49Z", "price": 4756.50 } ] }
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Canonical index symbol — may differ from what you sent (`DXY` → `DX-Y.NYB`) |
| `date` | string | Quote time, RFC3339 UTC (e.g. `2026-01-15T14:26:49Z`) |
| `price` | float | Current price (close price) |

> **Check `date` before treating `price` as current** — it is the quote's own timestamp, not the time of
> your request.

> **Symbol:** case-insensitive and the `^` is optional (`spx` = `^SPX`). Aliases resolve as listed below;
> anything else must be a canonical symbol from `GET /api/v1/macro/index/symbols`
> (`macro-index-symbol-list.md`).

**Common indexes and aliases**

| Index | Alias | Resolves to |
|-------|-------|-------------|
| S&P 500 | `GSPC`, `SP500`, `SPX500`, `US500` | `^SPX` |
| Dow Jones Industrial Average | — | `^DJI` |
| NASDAQ Composite | — | `^IXIC` |
| NASDAQ 100 | `NASDAQ100`, `NDX100` | `^NDX` |
| Russell 2000 | — | `^RUT` |
| CBOE Volatility Index | — | `^VIX` |
| US Dollar Index | `DXY`, `USDX`, `USDOLLAR` | `DX-Y.NYB` |
| Nikkei 225 | `NIKKEI` | `^N225` |
| Treasury yield, 10 years | `10Y`, `US10Y` | `^TNX` |
| Treasury yield, 30 years | `30Y` | `^TYX` |
| Treasury yield, 5 years | `5Y` | `^FVX` |
| Treasury bill, 13 weeks | `3M` | `^IRX` |

---
