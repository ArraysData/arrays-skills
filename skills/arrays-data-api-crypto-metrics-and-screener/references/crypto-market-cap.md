# Market cap

`GET crypto/market-cap`

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of market-cap items.

> **Sort order:** `data` is sorted **ascending** by time (oldest first), so `data[-1]` is the latest market cap and `data[0]` is the earliest in the range. ⚠️ This is the *opposite* of the `metrics/*` series and `market-metrics` in this skill, which are newest-first.

**Each item in `data` (TokenMarketCapItem):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Symbol | `symbol` | string | Token symbol |
| Name | `name` | string | Token name (may be omitted) |
| Timestamp | `timestamp` | integer | Unix timestamp in seconds |
| Time | `time` | string | Formatted time in RFC 3339 / ISO 8601 UTC |
| Market cap | `market_cap` | number | Market capitalization in USD |
