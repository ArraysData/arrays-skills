# DRAM Contract Price

`GET /api/v1/other/semiconductor/dram-contract-price` — **monthly**.
Use a lookback window of at least 1–2 months when fetching the "latest" price.

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
    { "symbol": "DDR4 8Gb 1Gx8", "date": "2026-05-29",
      "high": 28, "low": 18, "avg": 20 }
  ],
  "request_id": "..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Product item identifier (same as `item`) |
| `date` | string | Price date (`YYYY-MM-DD`) |
| `high` | float | Highest contract price (USD) |
| `low` | float | Lowest contract price (USD) |
| `avg` | float | Average contract price (USD) |

## Valid `item` values

19 items. Item names differ from DRAM spot — no parentheses, and the list adds DDR2 and module-level SO-DIMM/U-DIMM rows.

| Item | Category |
|------|----------|
| `DDR2 1Gb 64Mx16` | DDR2 |
| `DDR2 512Mb 32Mx16` | DDR2 |
| `DDR3 1Gb 64Mx16` | DDR3 |
| `DDR3 2Gb 128Mx16` | DDR3 |
| `DDR3 4Gb 256Mx16` | DDR3 |
| `DDR4 4Gb 256Mx16` | DDR4 |
| `DDR4 8Gb 1Gx8` | DDR4 |
| `DDR4 8Gb 512Mx16` | DDR4 |
| `DDR4 16Gb 1Gx16` | DDR4 |
| `DDR4 16Gb 2Gx8` | DDR4 |
| `DDR4 8GB SO-DIMM` | DDR4 module |
| `DDR4 8GB U-DIMM` | DDR4 module |
| `DDR4 16GB SO-DIMM` | DDR4 module |
| `DDR4 16GB U-DIMM` | DDR4 module |
| `DDR5 16Gb 2Gx8` | DDR5 |
| `DDR5 8GB SO-DIMM` | DDR5 module |
| `DDR5 8GB U-DIMM` | DDR5 module |
| `DDR5 16GB SO-DIMM` | DDR5 module |
| `DDR5 16GB U-DIMM` | DDR5 module |

## Example

```python
import requests, os, calendar
from datetime import datetime, timezone

base = os.environ.get("ARRAYS_API_BASE_URL", "https://data-tools.prd.space.id")

def to_ts(y, m, d):  # Unix seconds, UTC — do NOT use datetime.timestamp()
    return calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple())

resp = requests.get(f"{base}/api/v1/other/semiconductor/dram-contract-price",
    params={"item": "DDR4 8Gb 1Gx8",
            "start_time": to_ts(2025, 1, 1), "end_time": to_ts(2026, 6, 1)},
    headers={"X-API-Key": os.environ["ARRAYS_API_KEY"]})
body = resp.json()
data = sorted(body["data"], key=lambda r: r["date"])  # flat wrapper; don't trust ordering
for row in data:
    print(f"{row['date']}: high={row['high']}, low={row['low']}, avg={row['avg']}")
```
