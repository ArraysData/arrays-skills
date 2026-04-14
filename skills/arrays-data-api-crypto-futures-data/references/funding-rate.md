# Funding Rate

`GET /api/v1/crypto/funding-rate`

Binance funding rates settle every **8 hours** at 00:00, 08:00, 16:00 UTC. Query for exact settlement times only.

**CRITICAL — Fallback for missing settlement times**: Some tokens only have data at certain settlement times (e.g., AAVE only has 00:00 UTC). If querying a specific settlement time returns **empty `data`**, you MUST immediately retry with a full-day range (`start_time=day_start, end_time=next_day_start`) and report any available funding rate for that day. Never output "No data" or "API_ERROR" without trying the full-day fallback first. Filter the results to match the target date's timestamp.

```python
from datetime import timedelta

# Fallback pattern for funding rate queries:
resp = requests.get(f"{base}/api/v1/crypto/funding-rate",
    params={"symbol": symbol, "start_time": target_ts, "end_time": target_ts + 3600},
    headers={"X-API-Key": key})
data = resp.json().get("data", [])
if not data:  # No data at requested time — fallback to full day
    day_start = to_ts(year, month, day, 0)
    # IMPORTANT: use timedelta to safely get next day (handles month boundaries like Nov 30 → Dec 1)
    next_day = datetime(year, month, day, tzinfo=timezone.utc) + timedelta(days=1)
    day_end = int(calendar.timegm(next_day.timetuple()))
    resp = requests.get(f"{base}/api/v1/crypto/funding-rate",
        params={"symbol": symbol, "start_time": day_start, "end_time": day_end},
        headers={"X-API-Key": key})
    data = resp.json().get("data", [])
    # Filter for target date
    data = [d for d in data if d["time"].startswith(f"{year}-{month:02d}-{day:02d}")]
if data:
    print(data[0]["funding_rate"])
```

```json
{
  "success": true,
  "data": [
    { "symbol": "BTCUSDT", "funding_rate": 0.0001, "timestamp": 1723507200, "time": "2025-08-13T00:00:00Z" }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Trading pair symbol |
| `funding_rate` | float64 | Funding rate value. Positive means longs pay shorts; negative means shorts pay longs. |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | ISO 8601 / RFC 3339 time string (e.g. `2025-08-13T00:00:00Z`) |

---
