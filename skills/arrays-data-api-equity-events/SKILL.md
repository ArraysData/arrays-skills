---
name: arrays-data-api-equity-events
description: Guides the agent to call Arrays REST APIs for equity events (dividends, splits, earnings calendar, earnings transcripts, SEC earnings releases, IPO, M&A, equity offering, crowdfunding). Use when the user needs upcoming or historical corporate event dates, earnings call transcripts, or SEC-filed earnings release documents. earnings-calendar only covers upcoming and recent earnings (no historical data). To look up historical earnings reports or financials, use arrays-data-api-equity-fundamentals instead.
---

# Arrays Data API — Equity Events

**Domain**: `equity_events`. Dividends, stock splits, earnings calendar, earnings transcripts, SEC earnings releases, IPO calendar, mergers & acquisitions, equity offering, and crowdfunding.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Response wrapper formats

Endpoints use **two different** response wrappers:

**V2 format** (dividends, splits, earnings-calendar, earnings-transcript, sec-earnings-release) — data in `data` field:
```json
{ "success": true, "data": [ ... ] }
```
Access in Python: `body["data"]`

**Standard format** (ipo-calendar, ipo-confirmed-calendar) — data in `response` field:
```json
{ "success": true, "response": { "events": [...] } }
```
Access in Python: `body["response"]`

## Important notes

- **Use wide time windows**: When querying dividends or splits for a specific date, **ALWAYS** use a broad time range (at least +/- 90 days around the target date). A 1-day or even 7-day window will often return ZERO results because the API's internal timestamps don't align exactly with the event date. Always query a wide window and filter results client-side by matching the `date` field.
- **Dividend date types**: The `date` field is the ex-dividend date. `recordDate` is the record date. `paymentDate` is the payment date. These can differ by weeks (e.g., ex-date Mar 5 vs payment date Mar 27). When a user asks about a dividend "on" a specific date, check ALL date fields (`date`, `recordDate`, `paymentDate`) against that date since the user might be referring to any of them.
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
  - `mergers-acquisitions-rss` — M&A RSS feed
  - `equity-offering` — equity/fundraising offerings
  - `crowdfunding/offerings` — crowdfunding offerings

## Parameters by endpoint

### 1. `GET /api/v1/stocks/dividends`

PIT (Point-in-Time) dividend data for a specific symbol within a time range.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, MSFT, KO) |
| `start_time` | integer | Yes | Start timestamp (Unix seconds, UTC) |
| `end_time` | integer | Yes | End timestamp (Unix seconds, UTC) |
| `time_type` | string | Yes | Date type to filter by. One of: `RECORD_DATE`, `PAYMENT_DATE`, `DECLARATION_DATE` |
| `limit` | integer | No | Maximum number of results (1-1000, default: 50) |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | Ex-dividend date (YYYY-MM-DD) |
| `recordDate` | string | Record date (YYYY-MM-DD) |
| `paymentDate` | string | Payment date (YYYY-MM-DD) |
| `declarationDate` | string | Declaration date (YYYY-MM-DD) |
| `adjDividend` | number | Adjusted dividend amount |
| `dividend` | number | Dividend amount |
| `yield` | number | Dividend yield percentage |
| `frequency` | string | Dividend frequency (e.g., "Quarterly", "Monthly") |

---

### 2. `GET /api/v1/stocks/splits`

PIT (Point-in-Time) stock split data for a specific symbol within a time range.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, TSLA, NVDA) |
| `start_time` | integer | Yes | Start timestamp (Unix seconds, UTC) |
| `end_time` | integer | Yes | End timestamp (Unix seconds, UTC) |
| `limit` | integer | No | Maximum number of results (1-1000, default: 50) |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | Split date (YYYY-MM-DD) |
| `numerator` | number | Split numerator (e.g., 2.0 for a 2-for-1 split) |
| `denominator` | number | Split denominator (e.g., 1.0 for a 2-for-1 split) |

---

### 3. `GET /api/v1/stocks/earnings-calendar`

Earnings calendar data with optional filtering by symbol and/or date range.

**No historical data**: `earnings-calendar` only covers upcoming/recent earnings. Past earnings entries are replaced once the actual report is filed. For historical earnings filings, use `arrays-data-api-equity-fundamentals`.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | No | Stock symbol (e.g., AAPL, MSFT) - optional |
| `start_date` | string | No | Start date (YYYY-MM-DD format) - optional, requires end_date |
| `end_date` | string | No | End date (YYYY-MM-DD format) - optional, requires start_date |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier |
| `symbol` | string | Stock symbol |
| `date` | string | Earnings date (YYYY-MM-DD) |
| `eps` | string | Actual earnings per share |
| `eps_estimated` | string | Estimated earnings per share |
| `time` | string | Earnings call time (e.g., "AMC", "BMO") |
| `revenue` | string | Actual revenue |
| `revenue_estimated` | string | Estimated revenue |
| `fiscal_date_ending` | string | Fiscal period end date |
| `updated_from_date` | string | Date the data was updated from |
| `status` | string | Earnings status |
| `created_at` | string | Record creation timestamp |
| `updated_at` | string | Record last-update timestamp |

---

### 4. `GET /api/v1/stocks/earnings-transcript`

Full text of a company's earnings call, organized by speaker and section, for a specific fiscal period.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, MSFT) |
| `period_type` | string | Yes | Period type: `annual` or `quarterly` |
| `fiscal_year` | integer | Yes | Fiscal year (minimum: 2005, e.g., 2024) |
| `fiscal_quarter` | string | No | Fiscal quarter: `Q1`, `Q2`, `Q3`, `Q4` — required when period_type is `quarterly` |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol (e.g., AAPL) |
| `quarter` | string | Fiscal period identifier (e.g., "2024 Q1" for quarterly, "2024" for annual) |
| `transcript` | array | Array of transcript sections |

Each transcript section:

| Field | Type | Description |
|-------|------|-------------|
| `section` | string | Section name (e.g., "MANAGEMENT DISCUSSION SECTION") |
| `content` | array | Array of transcript entries |

Each transcript entry:

| Field | Type | Description |
|-------|------|-------------|
| `speaker` | string | Speaker name (e.g., "Arvind Krishna") |
| `title` | string | Speaker title/role (e.g., "CEO", "Analyst") |
| `content` | string | Transcript content/speech text |

---

### 5. `GET /api/v1/stocks/sec-earnings-release`

Retrieve the SEC earnings release publication date and filing URL for a company's official earnings report, filed with the SEC for a specific fiscal period.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, IBM) |
| `period_type` | string | Yes | `annual` or `quarter` |
| `fiscal_year` | integer | Yes | Fiscal year (e.g., 2024) |
| `fiscal_quarter` | integer | No | Fiscal quarter (1–4) — required when period_type is `quarter` |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `quarter` | string | Fiscal period identifier (e.g., "202401" = fiscal year 2024, Q1) |
| `release_date` | string | SEC publication date (YYYY-MM-DD) |
| `url` | string | URL to the SEC filing document |

---

### 6. `GET /api/v1/stocks/ipo-calendar`

Upcoming IPO schedules with company details, expected pricing, and market information.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from` | string | No | Start date in YYYY-MM-DD format (e.g., 2025-04-24) |
| `to` | string | No | End date in YYYY-MM-DD format (e.g., 2025-07-24) |

**Response fields** (each object in `events[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | IPO date (YYYY-MM-DD) |
| `daa` | string | IPO date-time (ISO 8601) |
| `company` | string | Company name |
| `exchange` | string | Exchange (e.g., "NYSE") |
| `actions` | string | Status (e.g., "Expected") |
| `shares` | integer | Number of shares offered (may be null) |
| `price_range` | string | Expected price range (may be null) |
| `market_cap` | string | Expected market cap (may be null) |

---

### 7. `GET /api/v1/stocks/ipo-confirmed-calendar`

Companies that have officially filed IPO documents with regulatory authorities.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from` | string | No | Start date in YYYY-MM-DD format (e.g., 2023-01-01) |
| `to` | string | No | End date in YYYY-MM-DD format (e.g., 2023-12-31) |

**Response fields** (each object in `events[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `cik` | string | SEC CIK number |
| `form` | string | Filing form type (e.g., "CERT") |
| `filingDate` | string | Filing date (YYYY-MM-DD) |
| `acceptedDate` | string | Accepted date-time (YYYY-MM-DD HH:MM:SS) |
| `effectivenessDate` | string | Effectiveness date (YYYY-MM-DD) |
| `url` | string | SEC filing document URL |

---

### 8. `GET /api/v1/stocks/mergers-acquisitions`

Mergers and acquisitions events filtered by date range and/or symbol.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from` | string | No | Start date (YYYY-MM-DD, e.g., 2023-08-10) |
| `to` | string | No | End date (YYYY-MM-DD, e.g., 2023-08-11) |
| `symbol` | string | No | Stock symbol (e.g., AAPL, RIO, WLKP) |

**Response fields** (wrapper has `count` + `data[]`; each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `companyName` | string | Acquiring company name |
| `cik` | string | Acquiring company CIK number |
| `symbol` | string | Acquiring company stock symbol |
| `targetedCompanyName` | string | Target company name |
| `targetedCik` | string | Target company CIK number |
| `targetedSymbol` | string | Target company stock symbol |
| `transactionDate` | string | Transaction date (YYYY-MM-DD) |
| `acceptanceTime` | string | SEC filing acceptance time |
| `url` | string | SEC filing document URL |

---

### 9. `GET /api/v1/stocks/mergers-acquisitions-rss`

M&A RSS feed from SEC filings with pagination.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | integer | No | Page number for pagination, starts from 0. If not provided, defaults to page 0 |

**Response fields** (wrapper has `count` + `data[]`; each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `companyName` | string | Acquiring company name |
| `cik` | string | Acquiring company CIK number |
| `symbol` | string | Acquiring company stock symbol |
| `targetedCompanyName` | string | Target company name |
| `targetedCik` | string | Target company CIK number |
| `targetedSymbol` | string | Target company stock symbol |
| `transactionDate` | string | Transaction date (YYYY-MM-DD) |
| `acceptanceTime` | string | SEC filing acceptance time |
| `url` | string | SEC filing document URL |

---

### 10. `GET /api/v1/stocks/equity-offering`

Latest equity offerings, including new shares being issued by companies and exempt offerings and amendments.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | integer | Yes | Page number starting from 0 |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `cik` | string | SEC CIK number |
| `url` | string | SEC filing URL |
| `companyName` | string | Company name |
| `entityName` | string | Entity name |
| `fillingDate` | string | Filing date |
| `date` | string | Offering date (ISO 8601) |
| `formType` | string | SEC form type (e.g., "D") |
| `formSignification` | string | Form description (e.g., "Notice of Exempt Offering of Securities") |
| `issuerStreet` | string | Issuer street address |
| `issuerCity` | string | Issuer city |
| `issuerStateOrCountry` | string | Issuer state or country code |
| `issuerStateOrCountryDescription` | string | Issuer state or country full name |
| `issuerZipCode` | string | Issuer ZIP code |
| `issuerPhoneNumber` | string | Issuer phone number |
| `jurisdictionOfIncorporation` | string | Jurisdiction of incorporation |
| `entityType` | string | Entity type (e.g., "Limited Partnership") |
| `incorporatedWithinFiveYears` | boolean | Whether incorporated within last five years |
| `yearOfIncorporation` | string | Year of incorporation |
| `relatedPersonFirstName` | string | Related person first name |
| `relatedPersonLastName` | string | Related person last name |
| `relatedPersonStreet` | string | Related person street address |
| `relatedPersonCity` | string | Related person city |
| `relatedPersonStateOrCountry` | string | Related person state or country code |
| `relatedPersonStateOrCountryDescription` | string | Related person state or country full name |
| `relatedPersonZipCode` | string | Related person ZIP code |
| `relatedPersonRelationship` | string | Related person relationship to issuer |
| `industryGroupType` | string | Industry group type |
| `revenueRange` | string | Revenue range |
| `federalExemptionsExclusions` | string | Federal exemptions/exclusions claimed |
| `isAmendment` | boolean | Whether this is an amendment filing |
| `dateOfFirstSale` | string | Date of first sale |
| `durationOfOfferingIsMoreThanYear` | boolean | Whether offering duration exceeds one year |
| `securitiesOfferedAreOfEquityType` | boolean | Whether securities offered are equity type |
| `isBusinessCombinationTransaction` | boolean | Whether this is a business combination |
| `minimumInvestmentAccepted` | integer | Minimum investment accepted (may be null) |
| `totalOfferingAmount` | integer | Total offering amount (may be null) |
| `totalAmountSold` | integer | Total amount sold (may be null) |
| `totalAmountRemaining` | integer | Total amount remaining (may be null) |
| `hasNonAccreditedInvestors` | boolean | Whether non-accredited investors participate |
| `totalNumberAlreadyInvested` | integer | Total number already invested (may be null) |
| `salesCommissions` | integer | Sales commissions (may be null) |
| `findersFees` | integer | Finders fees (may be null) |
| `grossProceedsUsed` | integer | Gross proceeds used (may be null) |
| `createdDate` | string | Record creation date |
| `updatedDate` | string | Record last-update date |
| `acceptanceTime` | string | SEC filing acceptance time |

---

### 11. `GET /api/v1/stocks/crowdfunding/offerings`

Paginated crowdfunding offerings information from SEC filings.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | integer | No | Page number (0-based, default: 0) |

**Response fields** (wrapper has `count` + `data[]`; each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `cik` | string | SEC CIK number |
| `company_name` | string | Company name |
| `url` | string | SEC filing URL |
| `form_type` | string | Form type (e.g., "C/A") |
| `form_signification` | string | Form description |
| `industry` | string | Industry (may be empty) |
| `filling_date` | string | Filing date |
| `date` | string | Offering date |
| `name_of_issuer` | string | Issuer name |
| `legal_status_form` | string | Legal form |
| `jurisdiction_organization` | string | Jurisdiction of organization |
| `issuer_street` | string | Issuer street address |
| `issuer_city` | string | Issuer city |
| `issuer_state_or_country` | string | Issuer state or country code |
| `issuer_zip_code` | string | Issuer ZIP code |
| `issuer_website` | string | Issuer website |
| `intermediary_company_name` | string | Intermediary company name |
| `intermediary_commission_cik` | string | Intermediary CIK number |
| `intermediary_commission_file_number` | string | Intermediary file number |
| `compensation_amount` | string | Compensation amount |
| `financial_interest` | string | Financial interest description |
| `security_offered_type` | string | Type of security offered |
| `security_offered_other_description` | string | Other security type description |
| `number_of_security_offered` | integer | Number of securities offered |
| `offering_price` | number | Offering price per security |
| `offering_amount` | number | Total offering amount |
| `over_subscription_accepted` | string | Whether over-subscription is accepted |
| `over_subscription_allocation_type` | string | Over-subscription allocation type |
| `maximum_offering_amount` | number | Maximum offering amount |
| `offering_deadline_date` | string | Offering deadline date |
| `current_number_of_employees` | number | Current employee count |
| `total_asset_most_recent_fiscal_year` | number | Total assets (most recent fiscal year) |
| `total_asset_prior_fiscal_year` | number | Total assets (prior fiscal year) |
| `cash_and_cash_equivalent_most_recent_fiscal_year` | number | Cash and equivalents (most recent fiscal year) |
| `cash_and_cash_equivalent_prior_fiscal_year` | number | Cash and equivalents (prior fiscal year) |
| `accounts_receivable_most_recent_fiscal_year` | number | Accounts receivable (most recent fiscal year) |
| `accounts_receivable_prior_fiscal_year` | number | Accounts receivable (prior fiscal year) |
| `short_term_debt_most_recent_fiscal_year` | number | Short-term debt (most recent fiscal year) |
| `short_term_debt_prior_fiscal_year` | number | Short-term debt (prior fiscal year) |
| `long_term_debt_most_recent_fiscal_year` | number | Long-term debt (most recent fiscal year) |
| `long_term_debt_prior_fiscal_year` | number | Long-term debt (prior fiscal year) |
| `revenue_most_recent_fiscal_year` | number | Revenue (most recent fiscal year) |
| `revenue_prior_fiscal_year` | number | Revenue (prior fiscal year) |
| `cost_goods_sold_most_recent_fiscal_year` | number | Cost of goods sold (most recent fiscal year) |
| `cost_goods_sold_prior_fiscal_year` | number | Cost of goods sold (prior fiscal year) |
| `taxes_paid_most_recent_fiscal_year` | number | Taxes paid (most recent fiscal year) |
| `taxes_paid_prior_fiscal_year` | number | Taxes paid (prior fiscal year) |
| `net_income_most_recent_fiscal_year` | number | Net income (most recent fiscal year) |
| `net_income_prior_fiscal_year` | number | Net income (prior fiscal year) |
| `updated_at` | string | Last update timestamp |
| `created_at` | string | Creation timestamp |
| `acceptance_time` | string | SEC filing acceptance time |

## Python examples

```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# Dividends (V2 format — use body["data"])
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

# Earnings calendar (V2 format — use body["data"])
resp = requests.get(f"{base}/api/v1/stocks/earnings-calendar",
    params={"symbol": "AAPL", "start_date": "2025-01-01", "end_date": "2025-06-30"},
    headers={"X-API-Key": key})
body = resp.json()
for e in body["data"]:
    print(f"{e['date']}: EPS={e['eps']}, Revenue={e['revenue']}")

# Earnings transcript (V2 format — use body["data"])
resp = requests.get(f"{base}/api/v1/stocks/earnings-transcript",
    params={"symbol": "AAPL", "period_type": "quarterly",
            "fiscal_year": 2024, "fiscal_quarter": "Q2"},
    headers={"X-API-Key": key})
body = resp.json()
for section in body["data"][0]["transcript"]:
    print(f"--- {section['section']} ---")
    for entry in section["content"]:
        print(f"{entry['speaker']} ({entry['title']}): {entry['content'][:100]}")

# SEC earnings release (V2 format — use body["data"])
resp = requests.get(f"{base}/api/v1/stocks/sec-earnings-release",
    params={"symbol": "IBM", "period_type": "quarter",
            "fiscal_year": 2024, "fiscal_quarter": 1},
    headers={"X-API-Key": key})
body = resp.json()
for r in body["data"]:
    print(f"{r['symbol']} {r['quarter']}: released {r['release_date']}, url={r['url']}")

# IPO calendar (Standard format — use body["response"])
resp = requests.get(f"{base}/api/v1/stocks/ipo-calendar",
    params={"from": "2025-01-01", "to": "2025-03-31"},
    headers={"X-API-Key": key})
body = resp.json()
events = body["response"]
```
