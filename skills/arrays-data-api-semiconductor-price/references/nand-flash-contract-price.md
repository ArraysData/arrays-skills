# NAND Flash Contract Price

`GET /api/v1/other/semiconductor/nand-flash-contract-price` — **monthly**.
Use a lookback window of at least 1–2 months when fetching the "latest" price.

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
    { "symbol": "NAND 128Gb 16Gx8 MLC", "date": "2026-05-29",
      "high": 26.85, "low": 26.2, "avg": 26.508 }
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

9 items. Naming differs from NAND spot: prefixed `NAND`, density-organisation-type order, and `Gx8` (not the spot `GBx8`).

| Item | Category |
|------|----------|
| `NAND 1Gb 128Mx8 SLC` | SLC |
| `NAND 2Gb 256Mx8 SLC` | SLC |
| `NAND 4Gb 512Mx8 SLC` | SLC |
| `NAND 8Gb 1024Mx8 SLC` | SLC |
| `NAND 16Gb 2Gx8 SLC` | SLC |
| `NAND 32Gb 4Gx8 SLC` | SLC |
| `NAND 32Gb 4Gx8 MLC` | MLC |
| `NAND 64Gb 8Gx8 MLC` | MLC |
| `NAND 128Gb 16Gx8 MLC` | MLC |

## Example

```python
import requests, os, calendar
from datetime import datetime, timezone

base = os.environ.get("ARRAYS_API_BASE_URL", "https://data-tools.prd.arrays.org")

def to_ts(y, m, d):  # Unix seconds, UTC — do NOT use datetime.timestamp()
    return calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple())

resp = requests.get(f"{base}/api/v1/other/semiconductor/nand-flash-contract-price",
    params={"item": "NAND 128Gb 16Gx8 MLC",
            "start_time": to_ts(2025, 1, 1), "end_time": to_ts(2026, 6, 1)},
    headers={"X-API-Key": os.environ["ARRAYS_API_KEY"]})
body = resp.json()
data = sorted(body["data"], key=lambda r: r["date"])  # flat wrapper; rows come ascending by date (sorting defensively is harmless)
for row in data:
    print(f"{row['date']}: high={row['high']}, low={row['low']}, avg={row['avg']}")
```
