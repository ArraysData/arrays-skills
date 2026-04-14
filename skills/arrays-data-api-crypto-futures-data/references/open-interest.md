# Open Interest

`GET /api/v1/crypto/open-interest`

```json
{
  "success": true,
  "data": [
    { "symbol": "ETHUSDT", "sum_open_interest_value": 10838759439, "timestamp": 1723507200, "time": "2025-08-14T00:00:00Z" }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Trading pair symbol |
| `sum_open_interest_value` | float64 | Total open interest value in USD |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | ISO 8601 / RFC 3339 time string |

---
