# 5. Symbol lists

`GET /api/v1/macro/index/symbols`

No request parameters. Returns the full index roster — the authoritative list of what
`index/historical` and `index/real-time` accept.

**Response** — `data` is an array of symbol objects:
```json
{ "success": true, "request_id": "...", "data": [ { "id": 2, "symbol": "DX-Y.NYB", "name": "US Dollar Index", "exchange": "ICEF", "currency": "USD", "created_at": "2026-03-24T10:33:31Z", "updated_at": "2026-04-03T06:58:06Z" } ] }
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Roster row id |
| `symbol` | string | Canonical symbol |
| `name` | string | Index name (e.g. `NASDAQ 100`) |
| `exchange` | string | Exchange code (nullable) |
| `currency` | string | Currency code (nullable) |
| `created_at` | string | RFC3339 UTC |
| `updated_at` | string | RFC3339 UTC |

---
