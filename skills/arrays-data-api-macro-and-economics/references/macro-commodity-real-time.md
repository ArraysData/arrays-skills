# 4. Real-time data

`GET /api/v1/macro/commodity/real-time`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Symbol identifier |

**Response** — `data` is an array:
```json
{ "success": true, "request_id": "...", "data": [ { "symbol": "GCUSD", "date": "2026-01-15T14:26:49Z", "price": 2650.00 } ] }
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Symbol identifier |
| `date` | string | Quote time, RFC3339 UTC (e.g. `2026-01-15T14:26:49Z`) |
| `price` | float | Current price (close price) |

> **Check `date` before treating `price` as current** — it is the quote's own timestamp, not the time of
> your request.

> **Symbol:** exact and case-sensitive — `gcusd` and `GOLD` both return 400 (gold is `GCUSD`). Discover
> valid values with `GET /api/v1/macro/commodity/symbols`.

---
