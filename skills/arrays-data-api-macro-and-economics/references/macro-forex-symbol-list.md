# 5. Symbol lists

`GET /api/v1/macro/forex/symbols`

No request parameters. Returns all available forex symbols.

**Response** — `data` is an array of symbol objects:
```json
{ "success": true, "request_id": "...", "data": [ { "symbol": "EURUSD", "from_currency": "EUR", ... } ] }
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Forex pair symbol (e.g. `ARSMXN`) |
| `from_currency` | string | Base currency code |
| `to_currency` | string | Quote currency code |
| `from_name` | string | Base currency name |
| `to_name` | string | Quote currency name |

---
