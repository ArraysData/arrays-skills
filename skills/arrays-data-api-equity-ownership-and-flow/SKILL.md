---
name: arrays-data-api-equity-ownership-and-flow
description: Guides the agent to call Arrays REST APIs for equity ownership and flow (institutional holdings, insider transactions, congress trades). Use when the user needs data about who owns a stock or recent insider/congress trading activity.
---


# Arrays Data API — Equity Ownership and Flow

**Domain**: `equity_ownership_and_flow`. Institutional holdings, insider transactions, and congress trades.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Response format

All endpoints return V2 format with a **flat `data` array**:
```json
{ "success": true, "data": [ ... ] }
```

Access data in Python: `body["data"]`

## Important notes

- **Handle empty results explicitly**: When the API returns an empty `data` array (no trades found), output **"Zero"** or **"0"** — never output "N/A", "No data", or "None". An empty result means zero trades/shares, not missing data.
- **Timestamp Rule**: Date fields are stored in US Eastern time (ET). To include a full day's data, set `end_time` to the last second of the day in ET — e.g. for 2024-12-31: `end_time = datetime(2024, 12, 31, 23, 59, 59, tzinfo=ET).timestamp()`
- **Null-safe field access**: `price` may be empty string or `"0"` in some records. Always use `.get()` with a default and guard before converting to `float`.
- **Use tight date ranges for insider trades**: When searching for insider trades on a specific date with `time_type=TRANSACTION_DATE`, use ONLY that date as the range (start=target_day, end=next_day). Do NOT use wide time windows — a wide range with limit=1000 will fill up with other dates' trades and miss the target date. Only use wider ranges when you're uncertain about the exact transaction date (e.g., when using `time_type=FILING_DATE`).

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `institution-holder` | `institution-holder` | Institution Holder |
| GET | `congress/recent-trades` | `congress-recent-trades` | Congress/Senate Trade |
| GET | `insider/transactions` | `insider-transactions` | Insider Trade |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Python example

```python
import requests, os
from datetime import datetime
from zoneinfo import ZoneInfo
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

ET = ZoneInfo("America/New_York")
def to_ts(y, m, d): return int(datetime(y, m, d, tzinfo=ET).timestamp())

# Get insider trades for AAPL on Apr 1, 2024
resp = requests.get(f"{base}/api/v1/stocks/insider/transactions",
    params={"symbol": "AAPL", "start_time": to_ts(2024, 4, 1), "end_time": to_ts(2024, 4, 2),
            "time_type": "TRANSACTION_DATE", "limit": 1000},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    trades = body["data"]  # flat array of insider trades
    for t in trades:
        shares = float(t.get('amount', 0) or 0)
        price = float(t.get('price', 0) or 0)
        code = t.get('transaction_code', '')
        side = 'Purchase' if code == 'P' else 'Sale' if code == 'S' else code
        print(f"{t['owner_name']}: {side} {abs(shares):.0f} shares at ${price}")

# Get congress trades for NVDA
resp = requests.get(f"{base}/api/v1/stocks/congress/recent-trades",
    params={"symbol": "NVDA", "start_time": 1719792000, "end_time": 1727654400,
            "time_type": "TRANSACTION_DATE", "limit": 100},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    trades = body["data"]  # flat array of congress trades
    for t in trades:
        print(f"{t['name']}: {t['transaction_type']} {t['amounts']}")

# Get institutional holders for AAPL
resp = requests.get(f"{base}/api/v1/stocks/institution-holder",
    params={"symbol": "AAPL", "start_time": 1719792000, "end_time": 1727654400,
            "time_type": "CALENDAR_END_DATE", "limit": 20},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    holders = body["data"]  # flat array of holders
    for h in holders:
        print(f"{h['investor_name']}: {h['shares_number']} shares")
```
