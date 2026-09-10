---
name: arrays-data-api-equity-events
description: Guides the agent to call Arrays REST APIs for equity events (dividends, splits, earnings calendar, earnings transcripts, event transcripts for shareholder meetings / conference presentations / sales calls / guidance / special situations, SEC earnings releases, IPO, M&A, equity offering, crowdfunding). Use when the user needs upcoming or historical corporate event dates, transcripts of earnings calls or any other corporate event (AGM, conference presentation, sales & revenue call), or SEC-filed earnings release documents. earnings-calendar covers US listings from 2025-01-01 onward and reaches only about 30 days into the future, so it answers "when did X report" but rarely "when is the next report" beyond a month out. For the reported figures themselves, use arrays-data-api-equity-fundamentals.
---


# Arrays Data API — Equity Events

**Domain**: `equity_events`. Dividends, stock splits, earnings calendar, earnings transcripts, SEC earnings releases, IPO calendar, mergers & acquisitions, equity offering, and crowdfunding.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.arrays.org`)
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
- **IPO events** — coverage gaps to know about:
ipo-calendar includes forward-looking schedules. The actions field doesn't reliably flip to "listed" after a completed listing — if an IPO shows "Expected" on a past date, treat it as unknown, not as evidence of failure to list.
ipo-confirmed-calendar is SEC registration filings (currently all CERT). It's a reasonable proxy for "this company is going public soon" but not "this company has IPO'd." Coverage starts 2025-01-01.
- **Fiscal year ≠ calendar year** (`earnings-transcript`, `sec-earnings-release`): these endpoints are keyed by the company's *fiscal* `fiscal_year` + `fiscal_quarter`, not the calendar date. Many fiscal calendars are offset — e.g. Walmart's fiscal year ends in late January, so the quarter it reports in **May 2026** is **FY2027 Q1** (verified: WMT `fiscal_year=2027, fiscal_quarter=Q1` → released 2026-05-21), not "2026 Q2". When the user gives a calendar month/date (e.g. "the May 2026 earnings call"), first map it to the fiscal period before calling these endpoints: call `fiscal-dates/range` in **arrays-data-api-equity-fundamentals** with the calendar date range → it returns the matching `fiscal_year` + `fiscal_quarter`. Never assume fiscal = calendar.
- **`sec-earnings-release` freshness (lags the public release)**: this endpoint is sourced from SEC 8-K filings, which trail the public earnings release for two groups — **wire filers** (large caps reporting via Business Wire / GlobeNewswire + a call; 8-K ~1 day later) and **IR-only filers** (notably **Berkshire Hathaway BRK-A/BRK-B**; publish on their IR site 2–3 days before the 8-K). When the user wants the **latest** period and this endpoint returns `NOT_FOUND` *after* the scheduled report date (per `earnings-calendar`) has passed, see `references/sec-earnings-release.md` → "Freshness & live fallback when the SEC filing lags" for a labeled, best-effort IR/newswire fallback.
- **Data ordering**: event/calendar endpoints (`dividends`, `splits`, `earnings-calendar`, `earnings-transcript`, `equity-offering`, `crowdfunding/offerings`, `ipo-confirmed-calendar`, `mergers-acquisitions`) return **newest-first** (descending by their primary date). **Exception**: `ipo-calendar` is passed through from the upstream vendor with **no ordering guarantee** — sort client-side before taking "first" / "latest". Combined with the wide-window rule above, always filter/sort by the date field rather than trusting `data[0]`. `earnings-calendar` carries at most `limit` records per response (1,000 max and default) and is cut at the oldest end, so page with `offset`.
- **`event-transcripts` vs `earnings-transcript`**: `event-transcripts` and `event-transcripts/{event_id}` cover all six event types (`Earnings`, `AnalystsShareholdersMeeting`, `ConferencePresentation`, `SalesRevenue`, `SpecialSituation`, `Guidance`) queried by `symbol` + date range. `event-transcripts` returns metadata only — fetch full text via `event-transcripts/{event_id}`. `earnings-transcript` is for earnings call transcripts only, and is queried by `symbol` + the fiscal period (`period_type` + `fiscal_year` + `fiscal_quarter`). Both endpoints return the same section → speaker/title/content body structure.
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
  - `earnings-calendar` — earnings release dates, US listings, 2025-01-01 onward plus roughly the next 30 days
  - `earnings-transcript` — earnings call transcript (full text, by speaker and section)
  - `event-transcripts` — transcript list for all corporate event types (earnings, AGM, conference presentation, sales call, guidance, special situation), by symbol + date range
  - `event-transcripts/{event_id}` — full transcript text for one event
  - `sec-earnings-release` — SEC earnings release publication date and filing URL
  - `ipo-calendar` — IPO calendar
  - `ipo-confirmed-calendar` — SEC registration filings (currently all CERT, coverage starts 2025-01-01)
  - `mergers-acquisitions` — M&A events
  - `equity-offering` — equity/fundraising offerings
  - `crowdfunding/offerings` — crowdfunding offerings

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `dividends` | `dividends` | Dividends |
| GET | `splits` | `splits` | Splits |
| GET | `earnings-calendar` | `earnings-calendar` | Earnings Calendar |
| GET | `earnings-transcript` | `earnings-transcript` | Earnings Transcript |
| GET | `event-transcripts` | `event-transcripts` | Event Transcripts — list (all event types) |
| GET | `event-transcripts/{event_id}` | `event-transcripts` | Event Transcripts — full text |
| GET | `sec-earnings-release` | `sec-earnings-release` | Sec Earnings Release |
| GET | `ipo-calendar` | `ipo-calendar` | Ipo Calendar |
| GET | `ipo-confirmed-calendar` | `ipo-confirmed-calendar` | SEC registration filings (currently all CERT, coverage starts 2025-01-01) |
| GET | `mergers-acquisitions` | `mergers-acquisitions` | Mergers Acquisitions |
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

# Earnings calendar — event dates only (no financial figures).
# For actual EPS/revenue use arrays-data-api-equity-fundamentals
# (company/income-statements); for estimates use
# arrays-data-api-equity-estimates-and-targets (estimates-guidance).
resp = requests.get(f"{base}/api/v1/stocks/earnings-calendar",
    params={"symbol": "AAPL", "start_time": 1735689600, "end_time": 1751241600},
    headers={"X-API-Key": key})
body = resp.json()
for e in body["data"]:
    print(f"{e['date']} ({e['time']}): reports for fiscal period ending {e['fiscal_date_ending']}")

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

# Event transcripts — list events by date range, then fetch full text by event_id
resp = requests.get(f"{base}/api/v1/stocks/event-transcripts",
    params={"symbol": "GOOS", "event_type": "AnalystsShareholdersMeeting",
            "from": to_ts(2026, 7, 1), "to": to_ts(2026, 8, 11)},
    headers={"X-API-Key": key})
events = resp.json()["data"]  # metadata only, newest-first; [] if none in range
if events:
    resp = requests.get(f"{base}/api/v1/stocks/event-transcripts/{events[0]['event_id']}",
        headers={"X-API-Key": key})
    detail = resp.json()["data"][0]  # data is a single-element array
    for section in detail["transcript"]:
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
