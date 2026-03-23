---
name: arrays-data-api-macro-and-economics
description: Guides the agent to call Arrays REST APIs for macro and economics data (treasury rates, economic calendar/indicators, CPI, GDP, unemployment, inflation, consumer sentiment, macro index/forex/commodity, VIX). Use when the user asks about macroeconomic indicators, CPI release dates, economic data announcements, interest rates, forex, commodity prices (gold GCUSD, silver SILUSD, oil CLUSD), market index data (S&P 500 ^GSPC, Dow Jones ^DJI, Nasdaq ^IXIC), or VIX volatility indexes.
---

# Arrays Data API — Macro and Economics

**Domain**: `macro_and_economics_data`. Treasury rates, economic calendar, economic indicators, macro index/forex/commodity historical and real-time data, and VIX.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Response wrapper formats

This API uses **two** response wrapper formats depending on the endpoint:

**Format A (most endpoints)** — data is inside `response`:
```json
{ "success": true, "response": { "data": [...] } }
```
Access data in Python: `body["response"]["data"]`

**Format B (economic/indicators only)** — data is inside `data` array:
```json
{ "success": true, "data": [ { "series": {...}, "observations": [...] } ] }
```
Access data in Python: `body["data"][0]["observations"]`

Always check `body["success"]` before accessing data.

## Path prefix and endpoints

### Stocks prefix — `/api/v1/stocks/`
- **Paths** (all GET):
  - `economic/calendar` — economic calendar events **(Format A, `response` is a flat array)**
  - `economic/indicators` — economic indicators (CPI, GDP, unemployment, etc.) **(Format B)**
  - `macro/index/historical` — index historical data **(Format A)**
  - `macro/index/real-time` — index real-time data **(Format A)**
  - `macro/index/price` — index 1-min price **(Format A)**
  - `macro/index/filter` — filter index data **(Format A)**
  - `macro/forex/historical` — forex historical data **(Format A)**
  - `macro/forex/real-time` — forex real-time data **(Format A)**
  - `macro/forex/price` — forex 1-min price **(Format A)**
  - `macro/forex/symbol-list` — available forex symbols **(Format A)**
  - `macro/forex/filter` — filter forex data **(Format A)**
  - `macro/commodity/historical` — commodity historical data **(Format A)**
  - `macro/commodity/real-time` — commodity real-time data **(Format A)**
  - `macro/commodity/price` — commodity 1-min price **(Format A)**
  - `macro/commodity/symbol-list` — available commodity symbols **(Format A)**
  - `macro/commodity/filter` — filter commodity data **(Format A)**
  - `vix` — VIX historical data **(Format A)**

### Treasury prefix — `/api/v1/treasury/`
- **Paths** (all GET):
  - `rates` — US treasury yield rates **(Format A, `response.rates`)**

## Parameters by endpoint

---

### 1. Economic calendar (`economic/calendar`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `event` | string | no | Filter by event type (e.g. `GDP`) |
| `country` | string | no | Filter by country (e.g. `US`) |

**Response** — Format A. `response` is a **flat array** of event objects (not nested in `data`):
```json
{ "success": true, "response": [ { "id": 1, "date": "...", "event": "...", ... } ], "total": 5 }
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Record ID |
| `date` | string | Event date/time (ISO 8601, e.g. `2024-01-15T10:30:00Z`) |
| `country` | string | Country name |
| `event` | string | Event name |
| `currency` | string | Currency code |
| `previous` | float | Previous value (nullable) |
| `estimate` | float | Estimated value (nullable) |
| `actual` | float | Actual value (nullable) |
| `change` | float | Change from previous (nullable) |
| `impact` | string | Impact level: `High`, `Medium`, or `Low` |
| `change_percentage` | float | Change percentage (nullable) |
| `unit` | string | Unit of measurement (nullable) |
| `created_at` | string | Record creation timestamp |
| `updated_at` | string | Record update timestamp |

**Common event names**: When searching the calendar for specific events, note that event names may differ from the common term. For example:
- Fed interest rate / FOMC rate decision → search for "Interest Rate Decision" (NOT "FOMC Minutes" which has no rate value)
- CPI data → search for events containing "CPI"
- Jobs report → search for "Nonfarm Payrolls" or "Unemployment Rate"

Always filter broadly (check if event name *contains* keywords) and look at the `actual` field for the value. Ignore events where `actual` is null.

**Python example:**
```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]
resp = requests.get(f"{base}/api/v1/stocks/economic/calendar",
    params={"start_time": 1722470400, "end_time": 1725148800, "country": "US"},
    headers={"X-API-Key": key})
body = resp.json()
events = body["response"]  # flat array of events
for e in events:
    if e.get("actual") is not None:  # skip events without actual values
        print(e["date"], e["event"], e["actual"])
```

---

### 2. Economic indicators (`economic/indicators`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `indicator_type` | string | yes | Indicator type enum (see list below) |
| `time_type` | string | yes | Time filter type: `OBSERVED_AT` (filter by publish timestamp) or `CALENDAR_START_DATE` (filter by calendar date) |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds, must be > start_time) |

**Supported `indicator_type` values** (36 indicators):

- GDP indicators: `GDP`, `REAL_GDP`, `REAL_GDP_PER_CAPITA`
- Employment: `INITIAL_CLAIMS`, `UNEMPLOYMENT_RATE`, `TOTAL_NONFARM_PAYROLL`
- Interest rates: `FEDERAL_FUNDS`
- Inflation / prices: `CPI`, `CORE_CPI`, `INFLATION_RATE_YOY`, `PPI`
- Consumer: `CONSUMER_SENTIMENT`, `CONSUMER_INFLATION_EXPECTATIONS`, `RETAIL_SALES`
- Production: `DURABLE_GOODS`, `INDUSTRIAL_PRODUCTION`
- Recession: `SMOOTHED_RECESSION_PROBABILITIES`
- TIPS (Treasury Inflation-Indexed): `TIPS_2_YEAR`, `TIPS_5_YEAR`, `TIPS_10_YEAR`, `TIPS_20_YEAR`, `TIPS_30_YEAR`
- Volatility: `VIX`, `GOLD_VIX`, `CRUDE_OIL_VIX`, `RUSSELL_2000_VIX`
- Treasury yields: `TREASURY_YIELD_1_MONTH`, `TREASURY_YIELD_3_MONTH`, `TREASURY_YIELD_6_MONTH`, `TREASURY_YIELD_2_YEAR`, `TREASURY_YIELD_5_YEAR`, `TREASURY_YIELD_10_YEAR`, `TREASURY_YIELD_20_YEAR`, `TREASURY_YIELD_30_YEAR`

**Important tips for `time_type`:**
- Use `CALENDAR_START_DATE` to filter by the period the data refers to (e.g., January 2025 CPI = date `2025-01-01`).
- Use `OBSERVED_AT` to filter by the date the data was published/released.
- **If `CALENDAR_START_DATE` returns empty for a recent period**, try widening the window by +/- 30 days, or switch to `OBSERVED_AT`.
- **To check if a specific indicator was announced on a given date**: Use `time_type=OBSERVED_AT` with `start_time`/`end_time` covering that day. Then check the `date` field in the response to see which period the released data refers to.
- **CRITICAL: Always filter observations by the `date` field.** The `observations` array may contain data for multiple months/quarters. Do NOT blindly use `observations[0]` — instead, match the `date` field to the target period. For example, when querying January 2025 data, filter for `date` starting with `"2025-01"`:
```python
obs = [o for o in indicator["observations"] if o["date"].startswith("2025-01")]
value = obs[0]["value"] if obs else None
```

**Response** — Format B. Data is wrapped in `data` array containing one object with `series` and `observations`:
```json
{
  "success": true,
  "data": [
    {
      "series": { "name": "CPI", "title": "Consumer Price Index", "frequency": "Monthly", "units": "Index 1982-1984=100", ... },
      "observations": [
        { "date": "2024-12-01", "value": 315.605, "releaseDate": "2025-01-15", "observedAt": 1736899200 }
      ]
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `data[0].series.name` | string | Series ID (e.g. `GDP`) |
| `data[0].series.title` | string | Series title (e.g. `Gross Domestic Product`) |
| `data[0].series.seasonalAdjustment` | string | Seasonal adjustment type |
| `data[0].series.frequency` | string | Data frequency (e.g. `Quarterly`) |
| `data[0].series.units` | string | Data units (e.g. `Billions of Dollars`) |
| `data[0].series.notes` | string | Series notes/description (optional) |
| `data[0].observations[]` | array | Array of observation data points |
| `data[0].observations[].date` | string | Observation date (e.g. `2024-01-15`) |
| `data[0].observations[].value` | float | Indicator value |
| `data[0].observations[].releaseDate` | string | First release date (e.g. `2024-04-25`) |
| `data[0].observations[].observedAt` | integer | Observation publish timestamp (Unix seconds) |

**Python example:**
```python
import requests, os, calendar
from datetime import datetime, timezone
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# ALWAYS compute timestamps with datetime — never hardcode
def to_ts(y, m, d):
    return int(calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple()))

# Get CPI data for December 2024
resp = requests.get(f"{base}/api/v1/stocks/economic/indicators",
    params={"indicator_type": "CPI", "time_type": "CALENDAR_START_DATE",
            "start_time": to_ts(2024, 12, 1), "end_time": to_ts(2025, 1, 1)},
    headers={"X-API-Key": key})
body = resp.json()
indicator = body["data"][0]  # first (and only) element in data array
series = indicator["series"]
observations = indicator["observations"]
# IMPORTANT: Always filter by date — observations may contain multiple periods
target_obs = [o for o in observations if o["date"].startswith("2024-12")]
if target_obs:
    print(f"{target_obs[0]['date']}: {target_obs[0]['value']} (units: {series['units']})")
```

---

### 3. Historical data (`macro/index/historical`, `macro/forex/historical`, `macro/commodity/historical`)

These three endpoints share the same parameter and response structure (OHLCV daily bars).

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Symbol identifier. Index: e.g. `^GSPC`, `^DJI`, `^IXIC`. Forex: e.g. `EURUSD`, `GBPJPY`. Commodity: e.g. `GCUSD`, `HEUSX`, `SILUSD` |
| `start_date` | string | yes | Start date (YYYY-MM-DD format) |
| `end_date` | string | yes | End date (YYYY-MM-DD format) |

**Response** — Format A. Data is in `response.data`:
```json
{ "success": true, "response": { "data": [ { "symbol": "EURUSD", "date": "2025-08-18", "open": 1.166, "close": 1.166, ... } ] } }
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Symbol identifier |
| `date` | string | Date (YYYY-MM-DD) |
| `open` | float | Opening price |
| `high` | float | Highest price |
| `low` | float | Lowest price |
| `close` | float | Closing price |
| `volume` | integer | Trading volume |
| `change` | float | Price change (may be omitted) |
| `changePercent` | float | Price change percentage (may be omitted) |
| `vwap` | float | Volume-weighted average price (may be omitted) |

**Python example:**
```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]
# Get EURUSD historical data
resp = requests.get(f"{base}/api/v1/stocks/macro/forex/historical",
    params={"symbol": "EURUSD", "start_date": "2025-08-18", "end_date": "2025-08-18"},
    headers={"X-API-Key": key})
body = resp.json()
bars = body["response"]["data"]  # array of OHLCV bars
for bar in bars:
    print(f"{bar['date']}: close={bar['close']}")
```

---

### 4. Real-time data (`macro/index/real-time`, `macro/forex/real-time`, `macro/commodity/real-time`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Symbol identifier |

**Response** — Format A. Data is in `response.data`:
```json
{ "success": true, "response": { "data": { "symbol": "^GSPC", "date": "2025-01-15", "price": 4756.50 } } }
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Symbol identifier |
| `date` | string | Date (YYYY-MM-DD) |
| `price` | float | Current price (close price) |

> **Note:** When no data is available, the API returns default values: `{"symbol": "", "date": "", "price": 0}`.

---

### 5. 1-minute price data (`macro/index/price`, `macro/forex/price`, `macro/commodity/price`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Symbol identifier |
| `from` | integer | yes | Start timestamp (Unix timestamp in seconds) |
| `to` | integer | yes | End timestamp (Unix timestamp in seconds) |

**Response** — Format A. Data is in `response.data`:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Symbol identifier |
| `timestamp` | integer | Unix timestamp in seconds |
| `open` | float | Opening price |
| `high` | float | Highest price |
| `low` | float | Lowest price |
| `close` | float | Closing price |
| `volume` | integer | Trading volume (may be omitted) |

---

### 6. Filter data (`macro/index/filter`, `macro/forex/filter`, `macro/commodity/filter`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_date` | string | yes | Start date (YYYY-MM-DD format) |
| `end_date` | string | yes | End date (YYYY-MM-DD format) |
| `min_close` | number | no | Minimum close price |
| `max_close` | number | no | Maximum close price |
| `min_volume` | number | no | Minimum volume |
| `max_volume` | number | no | Maximum volume |
| `min_change` | number | no | Minimum price change |
| `max_change` | number | no | Maximum price change |
| `min_change_percent` | number | no | Minimum price change percentage |
| `max_change_percent` | number | no | Maximum price change percentage |
| `min_vwap` | number | no | Minimum VWAP |
| `max_vwap` | number | no | Maximum VWAP |

**Response** — Format A. Data is in `response.data`:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Symbol identifier |
| `date` | string | Date (YYYY-MM-DD) |
| `close` | string | Closing price (string) |
| `volume` | integer | Trading volume (may be omitted) |
| `change` | string | Price change (string) |
| `change_percent` | string | Price change percentage (string) |
| `vwap` | string | Volume-weighted average price (string) |

---

### 7. Symbol lists (`macro/forex/symbol-list`, `macro/commodity/symbol-list`)

No request parameters. Returns all available symbols.

**Response** — Format A. Data is in `response.data`:

#### Forex symbol list

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Forex pair symbol (e.g. `ARSMXN`) |
| `fromCurrency` | string | Base currency code |
| `toCurrency` | string | Quote currency code |
| `fromName` | string | Base currency name |
| `toName` | string | Quote currency name |

#### Commodity symbol list

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Commodity symbol (e.g. `HEUSX`) |
| `name` | string | Commodity name |
| `exchange` | string | Exchange name (nullable) |
| `tradeMonth` | string | Trade month |
| `currency` | string | Currency code |

---

### 8. VIX historical data (`vix`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_date` | string | yes | Start date (YYYY-MM-DD format) |
| `end_date` | string | yes | End date (YYYY-MM-DD format) |

**Response** — Format A. Data is in `response.data`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Record ID |
| `symbol` | string | VIX symbol (always `VIX`) |
| `date` | string | Date (YYYY-MM-DD) |
| `open` | float | Opening value |
| `high` | float | Highest value |
| `low` | float | Lowest value |
| `close` | float | Closing value |
| `volume` | integer | Trading volume |

---

### 9. Treasury rates (`rates`)

Path: `/api/v1/treasury/rates`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `from` | string | no | Start date (YYYY-MM-DD format). If omitted returns latest rates |
| `to` | string | no | End date (YYYY-MM-DD format) |

**Response** — Format A. Data is in `response.rates`:
```json
{ "success": true, "response": { "rates": [ { "date": "2025-01-15", "month1": 5.25, "year10": 4.50, ... } ] } }
```

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Rate date (YYYY-MM-DD) |
| `month1` | float | 1-Month treasury rate (nullable) |
| `month2` | float | 2-Month treasury rate (nullable) |
| `month3` | float | 3-Month treasury rate (nullable) |
| `month6` | float | 6-Month treasury rate (nullable) |
| `year1` | float | 1-Year treasury rate (nullable) |
| `year2` | float | 2-Year treasury rate (nullable) |
| `year3` | float | 3-Year treasury rate (nullable) |
| `year5` | float | 5-Year treasury rate (nullable) |
| `year7` | float | 7-Year treasury rate (nullable) |
| `year10` | float | 10-Year treasury rate (nullable) |
| `year20` | float | 20-Year treasury rate (nullable) |
| `year30` | float | 30-Year treasury rate (nullable) |

## Example

```python
import requests, os
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# Economic indicators — get US CPI
resp = requests.get(f"{base}/api/v1/stocks/economic/indicators",
    params={"indicator_type": "CPI", "time_type": "CALENDAR_START_DATE",
            "start_time": 1719792000, "end_time": 1722470400},
    headers={"X-API-Key": key})
body = resp.json()
obs = body["data"][0]["observations"]  # data is array, take first element
print(obs[0]["date"], obs[0]["value"])

# Commodity historical — get gold price
resp = requests.get(f"{base}/api/v1/stocks/macro/commodity/historical",
    params={"symbol": "GCUSD", "start_date": "2025-05-01", "end_date": "2025-05-01"},
    headers={"X-API-Key": key})
body = resp.json()
bars = body["response"]["data"]  # response wrapper, then data
print(bars[0]["close"])

# Treasury rates
resp = requests.get(f"{base}/api/v1/treasury/rates",
    params={"from": "2025-01-01", "to": "2025-03-01"},
    headers={"X-API-Key": key})
body = resp.json()
rates = body["response"]["rates"]  # response wrapper, then rates
print(rates[0]["year10"])

```
