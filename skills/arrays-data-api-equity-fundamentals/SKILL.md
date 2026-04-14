---
name: arrays-data-api-equity-fundamentals
description: Calls Arrays REST APIs for equity fundamentals — company profiles, executive compensation (salary, bonus, stock awards), income/balance/cashflow statements, shares float, outstanding shares, fiscal dates, and KPI. Use when the user asks about company details, executive pay, quarterly/annual financial statements, or earnings filings. Do NOT use for financial metrics (revenue TTM, net income TTM, EPS TTM, ROE, ROA, ROIC, margins, debt ratios, current/quick ratio) or market-level technical indicators (moving averages, EMA, RSI, MACD, Bollinger, VWAP, beta, volatility, PE ratio, PB ratio, PS ratio, dividend yield, enterprise value, EV/EBITDA, price changes) — those MUST use arrays-data-api-stock-metrics.
---


# Arrays Data API — Equity Fundamentals

Company profiles, financial statements, shares float, outstanding shares, fiscal dates, and KPI.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## CRITICAL: Fiscal and Calendar Quarter Mapping

Many companies have fiscal years that do NOT align with the calendar year.

**Default**: When there is no FY/CY qualifier (e.g., "what was AAPL's 20xx Qx earning?") → treat as **fiscal quarter**. Treat as calendar quarter only when the user says "Calendar Year", "CY", gives a specific month/date or gives an explicit range (e.g., "Jul 2025", "CY 2025", "as of March 2025", "Jan-Mar 2025"). To get company financials, when faced with a calendar quarter/year, first determine which fiscal quarter/year it corresponds to. **Never assume fiscal = calendar.**

**FY → CY** (what calendar dates does a fiscal quarter cover?):
- Call `fiscal-dates` with `fiscal_year` + `fiscal_quarter` → use `calendar_end` as the period end date.

**CY → FY** (which fiscal quarter does a calendar period fall in?):
- Call `fiscal-dates/range` with the calendar date range → returns `fiscal_year` + `fiscal_quarter`.

**Earnings announcement vs. filing date**:
- Full financials (statements) are typically filed **1 day after** the press earnings release / earnings call.
- When the question mentions "announcement date", "release date", or "publish date", add **1–2 days buffer** to look up the fiscal period.

**Quarterly vs. yearly results**:
- **For cash flow / income / balance statements**: When looking for quarterly results, remember to filter the returned `data` array to match the exact `period` (e.g., `Q2`) and `fiscal_year`, and exclude `FY` entries.

**`time_type` selection**:
- `CALENDAR_END_DATE` — filter by the calendar end date of the financial reporting period.
- `FILING_DATE` — filter by when the report was officially filed/published with the SEC (e.g., "reports filed in 2024", "filed on Feb 6"). Note: filing date is typically 1–2 days after the earnings release.
- `OBSERVED_AT` — filter by point-in-time data availability.

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `company/detail` | `company-detail` | Company detail |
| GET | `company/income-statements` | `company-income-statements` | Financial statements |
| GET | `company/balance-sheets` | `company-balance-sheets` | Financial statements |
| GET | `company/cashflow-statements` | `company-cashflow-statements` | Financial statements |
| GET | `company/executives` | `company-executives` | Executives info |
| GET | `company/kpi` | `company-kpi` | KPI |
| GET | `shares-float` | `shares-float` | Shares float |
| GET | `outstanding-shares` | `outstanding-shares` | Outstanding shares |
| GET | `fiscal-dates` | `fiscal-dates` | Fiscal dates |
| GET | `fiscal-dates/range` | `fiscal-dates-range` | Fiscal dates by range |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Response format

All endpoints return a unified envelope:

```json
{ "success": true, "request_id": "...", "data": [ ... ] }
```

`data` is **always** an array. Access in Python: `body["data"]`

## Python examples

```python
import requests, os
from datetime import datetime
from zoneinfo import ZoneInfo
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

ET = ZoneInfo("America/New_York")
def to_ts(y, m, d): return int(datetime(y, m, d, tzinfo=ET).timestamp())

# Income statements
resp = requests.get(f"{base}/api/v1/stocks/company/income-statements",
    params={"symbol": "AAPL", "start_time": to_ts(2024, 1, 1), "end_time": to_ts(2025, 1, 1),
            "period_type": "quarter"},
    headers={"X-API-Key": key})
body = resp.json()
statements = body["data"]  # array of income statement objects
for s in statements:
    print(f"Revenue: {s['revenue']}, Net Income: {s['net_income']}")

# KPI values
resp = requests.get(f"{base}/api/v1/stocks/company/kpi",
    params={"symbol": "HD", "fiscal_year": 2025, "fiscal_quarter": "Q3"},
    headers={"X-API-Key": key})
body = resp.json()
kpis = body["data"]  # array of KPI objects
for k in kpis:
    for m in k["metrics"]:
        print(f"{m['name']}: {m['value']}")

# Company detail
resp = requests.get(f"{base}/api/v1/stocks/company/detail",
    params={"symbol": "AAPL"},
    headers={"X-API-Key": key})
body = resp.json()
company = body["data"]  # array
print(f"Name: {company[0]['name']}, Sector: {company[0]['sector']}")

# Executives info
resp = requests.get(f"{base}/api/v1/stocks/company/executives",
    params={"symbol": "AAPL"},
    headers={"X-API-Key": key})
body = resp.json()
executives = body["data"]  # array of executive objects
for e in executives:
    print(f"{e['name_and_position']} ({e['year']}): salary={e['salary']}")
```
