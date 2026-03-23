---
name: arrays-data-api-equity-ownership-and-flow
description: Guides the agent to call Arrays REST APIs for equity ownership and flow (institutional holdings, insider trades, senate trades). Use when the user needs data about who owns a stock or recent insider/senate trading activity.
---

# Arrays Data API — Equity Ownership and Flow

**Domain**: `equity_ownership_and_flow`. Institutional holdings, insider trades, and senate trades.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Endpoints

- **Prefix**: `/api/v1/stocks/`
- **Paths** (all GET):
  - `institution-holder` — institutional holders
  - `company/senate-trade` — senate member stock trades
  - `company/insider-trade` — insider trading activity

## Response format

All endpoints return V2 format with a **flat `data` array**:
```json
{ "success": true, "data": [ ... ] }
```

Access data in Python: `body["data"]`

## Important notes

- **Handle empty results explicitly**: When the API returns an empty `data` array (no trades found), output **"Zero"** or **"0"** — never output "N/A", "No data", or "None". An empty result means zero trades/shares, not missing data.
- **Timestamp Rule**: Date fields are stored in US Eastern time (ET). To include a full day's data, set `end_time` to the first second of the next day in ET — e.g. for 2024-12-31: `end_time = datetime(2025, 1, 1, 0, 0, 0, tzinfo=ET).timestamp()`
- **Null-safe field access**: Fields like `securitiesTransacted` and `price` may be `null`/`None` in some records. Always use `.get()` with a default value and convert to `float` before arithmetic.
- **Deduplicate insider trade records**: The insider trade API may return duplicate records for the same transaction. Always deduplicate by creating a unique key from `(reportingName, transactionDate, securitiesTransacted, price)` before summing or counting. Example:
```python
seen = set()
unique_trades = []
for t in trades:
    key = (t.get('reportingName'), t.get('transactionDate'),
           t.get('securitiesTransacted'), t.get('price'))
    if key not in seen:
        seen.add(key)
        unique_trades.append(t)
```
- **Use tight date ranges for insider trades**: When searching for insider trades on a specific date with `time_type=TRANSACTION_DATE`, use ONLY that date as the range (start=target_day, end=next_day). Do NOT use wide time windows — a wide range with limit=50 will fill up with other dates' trades and miss the target date. Only use wider ranges when you're uncertain about the exact transaction date (e.g., when using `time_type=FILING_DATE`).

## Parameters by endpoint

### GET `institution-holder`

Retrieve institution holder information for a specified stock symbol.

#### Request parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (uppercase, e.g., TSM, AAPL, MSFT) |
| `start_time` | integer | Yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | Yes | End time (Unix timestamp in seconds) |
| `time_type` | string | Yes | Time type for filtering: `CALENDAR_END_DATE`, `FILING_DATE`, or `OBSERVED_AT` |
| `limit` | integer | No | Limit number of results (default: 50, max: 5000) |

#### Response

```json
{
  "success": true,
  "data": [
    {
      "calendarEndDate": "2024-06-30",
      "investorName": "VANGUARD GROUP INC",
      "symbol": "AAPL",
      "sharesNumber": 1255256,
      "marketValue": 26850000,
      "weight": 0.0452,
      "ownership": 0.0048,
      ...
    }
  ]
}
```

Each element in `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `calendarEndDate` | string | Date of the holding record |
| `cik` | string | CIK identifier |
| `filingDate` | string | Filing date |
| `investorName` | string | Name of the institutional investor |
| `symbol` | string | Stock symbol |
| `securityName` | string | Security name |
| `typeOfSecurity` | string | Type of security |
| `securityCusip` | string | Security CUSIP |
| `sharesType` | string | Shares type |
| `putCallShare` | string | Put/Call/Share indicator |
| `investmentDiscretion` | string | Investment discretion type |
| `industryTitle` | string | Industry title |
| `weight` | float64 | Portfolio weight |
| `lastWeight` | float64 | Previous portfolio weight |
| `changeInWeight` | float64 | Change in weight |
| `changeInWeightPercentage` | float64 | Change in weight percentage |
| `marketValue` | float64 | Market value |
| `lastMarketValue` | float64 | Previous market value |
| `changeInMarketValue` | float64 | Change in market value |
| `changeInMarketValuePercentage` | float64 | Change in market value percentage |
| `sharesNumber` | int64 | Number of shares held |
| `lastSharesNumber` | int64 | Previous number of shares held |
| `changeInSharesNumber` | int64 | Change in shares number |
| `changeInSharesNumberPercentage` | float64 | Change in shares number percentage |
| `quarterEndPrice` | float64 | Quarter end price |
| `avgPricePaid` | float64 | Average price paid |
| `isNew` | bool | Whether this is a new position |
| `isSoldOut` | bool | Whether position was sold out |
| `ownership` | float64 | Ownership percentage |
| `lastOwnership` | float64 | Previous ownership percentage |
| `changeInOwnership` | float64 | Change in ownership |
| `changeInOwnershipPercentage` | float64 | Change in ownership percentage |
| `holdingPeriod` | int32 | Holding period in quarters |
| `firstAdded` | string | First added date |
| `performance` | int64 | Performance value |
| `performancePercentage` | float64 | Performance percentage |
| `lastPerformance` | int64 | Previous performance value |
| `changeInPerformance` | int64 | Change in performance |
| `isCountedForPerformance` | bool | Whether counted for performance |
| `observedAt` | int64 | Observed timestamp (Unix seconds) |

---

### GET `company/senate-trade`

Retrieve stock trades made by US senators and representatives. Parameter priority: `symbol` > `name` > latest disclosures.

#### Request parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | No | Stock symbol |
| `name` | string | No | Politician name |
| `tag` | string | No | Chamber filter: `senate`, `house`, `all` (default: `all`) |
| `transaction_type` | string | No | Transaction type filter: `Purchase`, `Sale`, `Sale (Full)`, `Sale (Partial)` |
| `start_time` | integer | Yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | Yes | End time (Unix timestamp in seconds) |
| `time_type` | string | Yes | Filter time type: `TRANSACTION_DATE`, `DISCLOSURE_DATE`, or `OBSERVED_AT` |
| `limit` | integer | No | Maximum results (1-1000, default: 100) |

#### Response

```json
{
  "success": true,
  "data": [
    {
      "symbol": "NVDA",
      "firstName": "Tommy",
      "lastName": "Tuberville",
      "type": "Purchase",
      "amount": "$1,001 - $15,000",
      "transactionDate": "2024-04-15",
      ...
    }
  ]
}
```

Each element in `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `disclosureDate` | string | Date of disclosure filing |
| `transactionDate` | string | Date of actual trade |
| `observedAt` | int64 | Observed timestamp (Unix seconds) |
| `firstName` | string | Politician's first name |
| `lastName` | string | Politician's last name |
| `office` | string | Political office |
| `district` | string | Congressional district |
| `owner` | string | Asset ownership type |
| `assetDescription` | string | Detailed description of traded asset |
| `assetType` | string | Type of asset |
| `type` | string | Transaction type: `Purchase`, `Sale (Full)`, `Sale (Partial)` |
| `amount` | string | Trade amount range in USD |
| `capitalGainsOver200Usd` | string | Whether capital gains exceed $200 |
| `comment` | string | Additional disclosure comments |
| `link` | string | Link to official disclosure document |

---

### GET `company/insider-trade`

Returns insider trading filings within a time range. All filters are optional; combined with AND logic.

#### Request parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | No | Stock symbol (uppercase, e.g., AAPL) |
| `name` | string | No | Reporting person's name (fuzzy match) |
| `transaction_type` | string | No | Transaction type: `P-Purchase` or `S-Sale` |
| `start_time` | integer | Yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | Yes | End time (Unix timestamp in seconds) |
| `time_type` | string | Yes | Filter time type: `TRANSACTION_DATE`, `FILING_DATE`, or `OBSERVED_AT` |
| `limit` | integer | No | Limit (1-1000, default: 50) |

#### Response

```json
{
  "success": true,
  "data": [
    {
      "symbol": "AAPL",
      "reportingName": "COOK TIMOTHY D",
      "transactionType": "S-Sale",
      "securitiesTransacted": 108136,
      "price": 229.5,
      "transactionDate": "2025-04-15",
      ...
    }
  ]
}
```

Each element in `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `filingDate` | string | SEC filing date |
| `filingTimestamp` | int64 | Filing Unix timestamp |
| `transactionDate` | string | Transaction date |
| `reportingCik` | string | Reporting person's CIK |
| `transactionType` | string | Transaction type (`P-Purchase` or `S-Sale`) |
| `securitiesOwned` | float64 | Number of securities owned after transaction |
| `securitiesTransacted` | float64 | Number of securities transacted |
| `companyCik` | string | Company CIK |
| `reportingName` | string | Reporting person's name |
| `typeOfOwner` | string | Type of ownership |
| `link` | string | SEC filing link |
| `securityName` | string | Security name |
| `price` | float64 | Transaction price |
| `formType` | string | Form type |
| `acquisitionOrDisposition` | string | A (Acquisition) or D (Disposition) |
| `observedAt` | int64 | Observed timestamp (Unix seconds) |

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
resp = requests.get(f"{base}/api/v1/stocks/company/insider-trade",
    params={"symbol": "AAPL", "start_time": to_ts(2024, 4, 1), "end_time": to_ts(2024, 4, 2),
            "time_type": "TRANSACTION_DATE", "limit": 50},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    trades = body["data"]  # flat array of insider trades
    for t in trades:
        shares = float(t.get('securitiesTransacted', 0) or 0)
        price = float(t.get('price', 0) or 0)
        print(f"{t['reportingName']}: {t['transactionType']} "
              f"{shares} shares at ${price}")

# Get senator trades for NVDA
resp = requests.get(f"{base}/api/v1/stocks/company/senate-trade",
    params={"symbol": "NVDA", "start_time": 1719792000, "end_time": 1727654400,
            "time_type": "TRANSACTION_DATE", "limit": 50},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    trades = body["data"]  # flat array of senate trades
    total_trades = len(trades)
    print(f"Found {total_trades} senate trades for NVDA")

# Get institutional holders for AAPL
resp = requests.get(f"{base}/api/v1/stocks/institution-holder",
    params={"symbol": "AAPL", "start_time": 1719792000, "end_time": 1727654400,
            "time_type": "CALENDAR_END_DATE", "limit": 20},
    headers={"X-API-Key": key})
body = resp.json()
if body["success"]:
    holders = body["data"]  # flat array of holders
    for h in holders:
        print(f"{h['investorName']}: {h['sharesNumber']} shares")
```
