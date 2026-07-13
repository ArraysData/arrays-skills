# DXI Index

`GET /api/v1/other/semiconductor/dxi-index` — **daily** (trading days — Mon–Fri, excluding holidays).

TrendForce DRAMeXchange (DXI) index — a single composite series tracking the memory spot market. **No `item` parameter.**

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | int | yes | Start time — **Unix timestamp in seconds** |
| `end_time` | int | yes | End time — **Unix timestamp in seconds** |

## Response

Flat wrapper: rows are under `data` (not `response.data`). Sort by `date` yourself — ordering is not guaranteed.

```json
{
  "success": true,
  "data": [
    { "symbol": "DXI", "date": "2026-06-25", "value": 847482.12,
      "change": 3852.22, "change_pct": 0.46, "ma30": 750342.202, "ma60": 710557.665 }
  ],
  "request_id": "..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Always `DXI` |
| `date` | string | Index date (`YYYY-MM-DD`) |
| `value` | float | DXI index value |
| `change` | float | Day-over-day absolute change |
| `change_pct` | float | Day-over-day percent change |
| `ma30` | float | 30-day moving average |
| `ma60` | float | 60-day moving average |

## Example

```python
import requests, os, calendar
from datetime import datetime, timezone

base = os.environ.get("ARRAYS_API_BASE_URL", "https://data-tools.prd.space.id")

def to_ts(y, m, d):  # Unix seconds, UTC — do NOT use datetime.timestamp()
    return calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple())

resp = requests.get(f"{base}/api/v1/other/semiconductor/dxi-index",
    params={"start_time": to_ts(2026, 1, 1), "end_time": to_ts(2026, 6, 26)},
    headers={"X-API-Key": os.environ["ARRAYS_API_KEY"]})
body = resp.json()
data = sorted(body["data"], key=lambda r: r["date"])  # flat wrapper; don't trust ordering
for row in data:
    print(f"{row['date']}: value={row['value']}, change_pct={row['change_pct']}")
```
