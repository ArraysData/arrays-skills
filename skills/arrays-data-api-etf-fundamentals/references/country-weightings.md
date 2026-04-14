# ETF Country Weightings

`GET /api/v1/etf/country-weightings`

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | ETF symbol (uppercase, e.g., SPY, QQQ, IWM) |

**Response envelope:** `{ "success": true, "request_id": "...", "data": [ ... ] }`

Each object in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `country` | string | Country name (e.g., "United States") |
| `weight_percentage` | string | Percentage weight as a string (e.g., "99.56%") |

---
