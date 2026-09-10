# NAND Flash Spot Price

`GET /api/v1/other/semiconductor/nand-flash-spot-price` — **weekly** (published Mondays).
Use a lookback window of at least 2–3 weeks when fetching the "latest" price.

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `item` | string | yes | NAND Flash item name, case-sensitive (see valid values below) |
| `start_time` | int | yes | Start time — **Unix timestamp in seconds** |
| `end_time` | int | yes | End time — **Unix timestamp in seconds** |

## Response

Flat wrapper: rows are under `data` (not `response.data`). Rows are returned in ascending `date` order (oldest first) — note this is the opposite default of the macro historical endpoints, which are newest-first.

```json
{
  "success": true,
  "data": [
    { "symbol": "MLC 64Gb 8GBx8", "date": "2026-01-05",
      "high": 7.45, "low": 6.8, "avg": 7.113 }
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

9 items, snapshot 2026-06-10 — the live spec is authoritative (see SKILL.md Important notes):

| Item | Category |
|------|----------|
| `MLC 32Gb 4GBx8` | MLC |
| `MLC 64Gb 8GBx8` | MLC |
| `MLC 128Gb 16GBx8` | MLC |
| `MLC 256Gb 32GBx8` | MLC |
| `SLC 1Gb 128MBx8` | SLC |
| `SLC 2Gb 256MBx8` | SLC |
| `SLC 4Gb 512MBx8` | SLC |
| `SLC 8Gb 1GBx8` | SLC |
| `SLC 16Gb 2GBx8` | SLC |

## Example

```python
import requests, os, calendar
from datetime import datetime, timezone

base = os.environ.get("ARRAYS_API_BASE_URL", "https://data-tools.prd.arrays.org")

def to_ts(y, m, d):  # Unix seconds, UTC — do NOT use datetime.timestamp()
    return calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple())

resp = requests.get(f"{base}/api/v1/other/semiconductor/nand-flash-spot-price",
    params={"item": "MLC 64Gb 8GBx8",
            "start_time": to_ts(2025, 1, 1), "end_time": to_ts(2025, 3, 1)},
    headers={"X-API-Key": os.environ["ARRAYS_API_KEY"]})
body = resp.json()
data = sorted(body["data"], key=lambda r: r["date"])  # flat wrapper; rows come ascending by date (sorting defensively is harmless)
for row in data:  # weekly → ~4-5 rows per month, not ~20
    print(f"{row['date']}: high={row['high']}, low={row['low']}, avg={row['avg']}")
```
