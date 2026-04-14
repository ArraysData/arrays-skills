# Long Short Ratio

`GET /api/v1/crypto/long-short-ratio`

```json
{
  "success": true,
  "data": [
    { "symbol": "BTCUSDT", "long_short_ratio": 1.61, "timestamp": 1723507200, "time": "2025-08-13T00:00:00Z" }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Trading pair symbol |
| `long_short_ratio` | float64 | Long/short ratio. >1.0 means more long; <1.0 means more short. |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | ISO 8601 / RFC 3339 time string |

---
