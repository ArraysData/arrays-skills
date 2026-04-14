# 5. Symbol lists

`GET /api/v1/macro/commodity/symbols`

No request parameters. Returns all available commodity symbols.

**Response** — `data` is an array of symbol objects:
```json
{ "success": true, "request_id": "...", "data": [ { "symbol": "GCUSD", "name": "Gold", ... } ] }
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Commodity symbol (e.g. `HEUSX`) |
| `name` | string | Commodity name |
| `exchange` | string | Exchange name (nullable) |
| `trade_month` | string | Trade month |
| `currency` | string | Currency code |

---
