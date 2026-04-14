# Market cap

`GET crypto/market-cap`

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of market-cap items.

**Each item in `data` (TokenMarketCapItem):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Symbol | `symbol` | string | Token symbol |
| Name | `name` | string | Token name (may be omitted) |
| Timestamp | `timestamp` | integer | Unix timestamp in seconds |
| Time | `time` | string | Formatted time in RFC 3339 / ISO 8601 UTC |
| Market cap | `market_cap` | number | Market capitalization in USD |
