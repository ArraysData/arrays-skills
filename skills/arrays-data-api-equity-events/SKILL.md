---
name: arrays-data-api-equity-events
description: Guides the agent to call Arrays REST APIs for equity events (dividends, splits, earnings calendar, earnings transcripts, SEC earnings releases, IPO, M&A, equity offering, crowdfunding). Use when the user needs upcoming or historical corporate event dates, earnings call transcripts, or SEC-filed earnings release documents. earnings-calendar only covers upcoming and recent earnings (no historical data). To look up historical earnings reports or financials, use arrays-data-api-equity-fundamentals instead.
---


# Arrays Data API — Equity Events

**Domain**: `equity_events`. Dividends, stock splits, earnings calendar, earnings transcripts, SEC earnings releases, IPO calendar, mergers & acquisitions, equity offering, and crowdfunding.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Response format

All endpoints return a unified envelope with a **`data` array**:
```json
{ "success": true, "request_id": "...", "data": [ ... ] }
```
Access in Python: `body["data"]`

## Important notes

- **Use wide time windows**: When querying dividends or splits for a specific date, **ALWAYS** use a broad time range (at least +/- 90 days around the target date). A 1-day or even 7-day window will often return ZERO results because the API's internal timestamps don't align exactly with the event date. Always query a wide window and filter results client-side by matching the `date` field.
- **Dividend date types**: The `date` field is the ex-dividend date. `record_date` is the record date. `payment_date` is the payment date. These can differ by weeks (e.g., ex-date Mar 5 vs payment date Mar 27). When a user asks about a dividend "on" a specific date, check ALL date fields (`date`, `record_date`, `payment_date`) against that date since the user might be referring to any of them.
- **Timestamp computation**: Always use Python `datetime` + `calendar` to compute Unix timestamps.
```python
import calendar
from datetime import datetime, timezone
ts = int(calendar.timegm(datetime(2025, 8, 13, 0, 0, 0, tzinfo=timezone.utc).timetuple()))
```

## Path prefix and endpoints

- **Prefix**: `/api/v1/stocks/`
- **Paths** (all GET):
  - `dividends` — dividend calendar (PIT)
  - `splits` — stock splits (PIT)
  - `earnings-calendar` — recent/upcoming earnings release dates, no historical data
  - `earnings-transcript` — earnings call transcript (full text, by speaker and section)
  - `sec-earnings-release` — SEC earnings release publication date and filing URL
  - `ipo-calendar` — IPO calendar
  - `ipo-confirmed-calendar` — confirmed IPO calendar
  - `mergers-acquisitions` — M&A events
  - `mergers-acquisitions/rss` — M&A RSS feed
  - `equity-offering` — equity/fundraising offerings
  - `crowdfunding/offerings` — crowdfunding offerings

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `dividends` | `dividends` | Dividends |
| GET | `splits` | `splits` | Splits |
| GET | `earnings-calendar` | `earnings-calendar` | Earnings Calendar |
| GET | `earnings-transcript` | `earnings-transcript` | Earnings Transcript |
| GET | `sec-earnings-release` | `sec-earnings-release` | Sec Earnings Release |
| GET | `ipo-calendar` | `ipo-calendar` | Ipo Calendar |
| GET | `ipo-confirmed-calendar` | `ipo-confirmed-calendar` | Ipo Confirmed Calendar |
| GET | `mergers-acquisitions` | `mergers-acquisitions` | Mergers Acquisitions |
| GET | `mergers-acquisitions/rss` | `mergers-acquisitions-rss` | Mergers Acquisitions Rss |
| GET | `equity-offering` | `equity-offering` | Equity Offering |
| GET | `crowdfunding/offerings` | `crowdfunding-offerings` | Crowdfunding — Offerings |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Python examples

```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# Dividends — use body["data"]
resp = requests.get(f"{base}/api/v1/stocks/dividends",
    params={"symbol": "AAPL", "start_time": 1704067200, "end_time": 1735689600,
            "time_type": "RECORD_DATE", "limit": 10},
    headers={"X-API-Key": key})
body = resp.json()
for d in body["data"]:
    print(f"{d['date']}: ${d['dividend']} (yield: {d['yield']}%)")

# Splits — use WIDE time range (+/- 90 days), then filter by date
import calendar
from datetime import datetime, timezone
def to_ts(y, m, d):
    return int(calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple()))

resp = requests.get(f"{base}/api/v1/stocks/splits",
    params={"symbol": "AAPL", "start_time": to_ts(2020, 6, 1),
            "end_time": to_ts(2020, 11, 30), "limit": 50},
    headers={"X-API-Key": key})
body = resp.json()
for s in body["data"]:
    if s["date"] == "2020-08-31":
        print(f"{int(s['numerator'])}-for-{int(s['denominator'])} split")

# Earnings calendar — use body["data"]
resp = requests.get(f"{base}/api/v1/stocks/earnings-calendar",
    params={"symbol": "AAPL", "start_time": 1735689600, "end_time": 1751241600},
    headers={"X-API-Key": key})
body = resp.json()
for day in body["data"]:
    for e in day["entries"]:
        print(f"{day['date']}: EPS={e['eps']}, Revenue={e['revenue']}")

# Earnings transcript — use body["data"]
resp = requests.get(f"{base}/api/v1/stocks/earnings-transcript",
    params={"symbol": "AAPL", "period_type": "quarterly",
            "fiscal_year": 2024, "fiscal_quarter": "Q2"},
    headers={"X-API-Key": key})
body = resp.json()
for section in body["data"][0]["transcript"]:
    print(f"--- {section['section']} ---")
    for entry in section["content"]:
        print(f"{entry['speaker']} ({entry['title']}): {entry['content'][:100]}")

# SEC earnings release — use body["data"]
resp = requests.get(f"{base}/api/v1/stocks/sec-earnings-release",
    params={"symbol": "IBM", "period_type": "quarterly",
            "fiscal_year": 2024, "fiscal_quarter": "Q2"},
    headers={"X-API-Key": key})
body = resp.json()
for r in body["data"]:
    print(f"{r['symbol']} {r['quarter']}: released {r['release_date']}, url={r['url']}")

# IPO calendar — use body["data"]
resp = requests.get(f"{base}/api/v1/stocks/ipo-calendar",
    params={"from": "2025-01-01", "to": "2025-03-31"},
    headers={"X-API-Key": key})
body = resp.json()
events = body["data"]
```
