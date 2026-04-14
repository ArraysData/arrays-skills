# ETF Holdings

`GET /api/v1/etf/holdings`

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | ETF symbol (uppercase, e.g., SPY, QQQ, IWM) |

**Response envelope:** `{ "success": true, "request_id": "...", "data": [ ... ] }`

Each object in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The parent ETF ticker symbol |
| `asset` | string | The ticker symbol of the held asset |
| `name` | string | Company or asset name |
| `isin` | string | International Securities Identification Number of the holding |
| `security_cusip` | string | CUSIP identifier of the holding |
| `shares_number` | int64 | Number of shares held |
| `weight_percentage` | float64 | Percentage weight of this holding in the portfolio |
| `market_value` | float64 | Total market value of the holding |
| `updated_at` | string | Last update timestamp |

---
