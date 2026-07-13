# DRAM Spot Price

`GET /api/v1/other/semiconductor/dram-spot-price` — **daily** (trading days — Mon–Fri, excluding holidays).

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `item` | string | yes | DRAM item name, case-sensitive (see valid values below) |
| `start_time` | int | yes | Start time — **Unix timestamp in seconds** |
| `end_time` | int | yes | End time — **Unix timestamp in seconds** |

## Response

Flat wrapper: rows are under `data` (not `response.data`). Sort by `date` yourself — ordering is not guaranteed.

```json
{
  "success": true,
  "data": [
    { "symbol": "DDR5 16Gb (2Gx8) 4800/5600", "date": "2026-01-02",
      "high": 42, "low": 21, "avg": 29.803 }
  ],
  "request_id": "..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Product item identifier (same as `item`) |
| `date` | string | Price date (`YYYY-MM-DD`) |
| `high` | float | Highest spot price (USD) |
| `low` | float | Lowest spot price (USD) |
| `avg` | float | Average spot price (USD) |

## Valid `item` values

19 items, snapshot 2026-06-10 — the live spec is authoritative (see SKILL.md Important notes):

| Item | Category |
|------|----------|
| `DDR3 2Gb 128Mx16 1600/1866` | DDR3 |
| `DDR3 2Gb 256Mx8 1600/1866` | DDR3 |
| `DDR3 4Gb 256Mx16 1600/1866` | DDR3 |
| `DDR3 4Gb 512Mx8 1600/1866` | DDR3 |
| `DDR3 4Gb 512Mx8 eTT` | DDR3 |
| `DDR4 4Gb (256Mx16) 2400/2666` | DDR4 |
| `DDR4 4Gb (512Mx8) 2400/2666` | DDR4 |
| `DDR4 4Gb 512Mx8 eTT` | DDR4 |
| `DDR4 8Gb (512Mx16) 2666` | DDR4 |
| `DDR4 8Gb (512Mx16) 3200` | DDR4 |
| `DDR4 8Gb (1Gx8) 2666` | DDR4 |
| `DDR4 8Gb (1Gx8) 3200` | DDR4 |
| `DDR4 8Gb (1Gx8) eTT` | DDR4 |
| `DDR4 16Gb (1Gx16) 3200` | DDR4 |
| `DDR4 16Gb (2Gx8) 2666` | DDR4 |
| `DDR4 16Gb (2Gx8) 3200` | DDR4 |
| `DDR4 16Gb (2Gx8) eTT` | DDR4 |
| `DDR5 16Gb (2Gx8) 4800/5600` | DDR5 |
| `DDR5 16Gb (2Gx8) eTT` | DDR5 |

## Example

```python
import requests, os, calendar
from datetime import datetime, timezone

base = os.environ.get("ARRAYS_API_BASE_URL", "https://data-tools.prd.space.id")

def to_ts(y, m, d):  # Unix seconds, UTC — do NOT use datetime.timestamp()
    return calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple())

resp = requests.get(f"{base}/api/v1/other/semiconductor/dram-spot-price",
    params={"item": "DDR5 16Gb (2Gx8) 4800/5600",
            "start_time": to_ts(2025, 1, 1), "end_time": to_ts(2025, 3, 1)},
    headers={"X-API-Key": os.environ["ARRAYS_API_KEY"]})
body = resp.json()
data = sorted(body["data"], key=lambda r: r["date"])  # flat wrapper; don't trust ordering
for row in data:
    print(f"{row['date']}: high={row['high']}, low={row['low']}, avg={row['avg']}")
```
