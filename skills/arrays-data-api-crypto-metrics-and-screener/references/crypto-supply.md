# Supply

`GET crypto/supply`

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of supply items.

**Each item in `data` (TokenSupplyItem):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Symbol | `symbol` | string | Token symbol |
| Name | `name` | string | Token name (may be omitted) |
| Timestamp | `timestamp` | integer | Unix timestamp in seconds |
| Time | `time` | string | Formatted time in RFC 3339 / ISO 8601 UTC |
| Circulating supply | `circulating_supply` | number | Current circulating supply |
| Total supply | `total_supply` | number | Total supply |
