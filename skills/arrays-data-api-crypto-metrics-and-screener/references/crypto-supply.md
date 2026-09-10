# Supply

`GET crypto/supply`

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of supply items.

> **Sort order:** `data` is sorted **ascending** by time (oldest first), so `data[-1]` is the latest supply and `data[0]` is the earliest in the range. ⚠️ This is the *opposite* of the `metrics/*` series and `market-metrics` in this skill, which are newest-first.

**Each item in `data` (TokenSupplyItem):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Symbol | `symbol` | string | Token symbol |
| Name | `name` | string | Token name (may be omitted) |
| Timestamp | `timestamp` | integer | Unix timestamp in seconds |
| Time | `time` | string | Formatted time in RFC 3339 / ISO 8601 UTC |
| Circulating supply | `circulating_supply` | number | Current circulating supply |
| Total supply | `total_supply` | number | Total supply |
