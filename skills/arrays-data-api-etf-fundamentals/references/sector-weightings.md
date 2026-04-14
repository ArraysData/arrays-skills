# ETF Sector Weightings

`GET /api/v1/etf/sector-weightings`

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | ETF symbol (uppercase, e.g., SPY, QQQ, IWM) |

**Response envelope:** `{ "success": true, "request_id": "...", "data": [ ... ] }`

Each object in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The ETF ticker symbol |
| `sector` | string | Sector name (e.g., "Technology", "Financial Services") |
| `weight_percentage` | float64 | Percentage weight as a number (e.g., 34.62) |

---
