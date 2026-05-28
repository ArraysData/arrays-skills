# 7. Treasury rates

`GET /api/v1/macro/treasury-rates`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | integer | no | Start time (Unix timestamp in seconds). If omitted returns latest rates |
| `end_time` | integer | no | End time (Unix timestamp in seconds). Must be strictly greater than `start_time` |

**Response** — `data` is an array of rate objects:
```json
{ "success": true, "request_id": "...", "data": [ { "date": "2025-01-15", "month1": 5.25, "year10": 4.50, ... } ] }
```
Access in Python: `body["data"]`

**Python example:**
```python
import requests, os, calendar
from datetime import datetime, timezone
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

def to_ts(y, m, d):
    return int(calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple()))

resp = requests.get(f"{base}/api/v1/macro/treasury-rates",
    params={"start_time": to_ts(2024, 8, 5), "end_time": to_ts(2024, 8, 6)},
    headers={"X-API-Key": key})
body = resp.json()
rates = body["data"]
target = [r for r in rates if r["date"] == "2024-08-05"]
if target:
    print(f"10-Year yield: {target[0]['year10']}%")
```

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Rate date (YYYY-MM-DD) |
| `month1` | float | 1-Month treasury rate (nullable) |
| `month2` | float | 2-Month treasury rate (nullable) |
| `month3` | float | 3-Month treasury rate (nullable) |
| `month6` | float | 6-Month treasury rate (nullable) |
| `year1` | float | 1-Year treasury rate (nullable) |
| `year2` | float | 2-Year treasury rate (nullable) |
| `year3` | float | 3-Year treasury rate (nullable) |
| `year5` | float | 5-Year treasury rate (nullable) |
| `year7` | float | 7-Year treasury rate (nullable) |
| `year10` | float | 10-Year treasury rate (nullable) |
| `year20` | float | 20-Year treasury rate (nullable) |
| `year30` | float | 30-Year treasury rate (nullable) |

---
