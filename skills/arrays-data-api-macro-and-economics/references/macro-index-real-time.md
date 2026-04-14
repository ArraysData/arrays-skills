# 4. Real-time data

`GET /api/v1/macro/index/real-time`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Symbol identifier |

**Response** — `data` is an array:
```json
{ "success": true, "request_id": "...", "data": [ { "symbol": "^SPX", "date": "2025-01-15", "price": 4756.50 } ] }
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Symbol identifier |
| `date` | string | Date (YYYY-MM-DD) |
| `price` | float | Current price (close price) |

> **Note:** When no data is available, the API returns default values: `{"symbol": "", "date": "", "price": 0}`.

---
