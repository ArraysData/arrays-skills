---
name: arrays-data-api-etf-fundamentals
description: Guides the agent to call Arrays REST APIs for ETF fundamentals (holdings, info, country/sector weightings, kline, fund flow). Use when the user needs ETF composition, performance, or flow data.
---

# Arrays Data API — ETF Fundamentals

**Domain**: `etf_fundamentals`. ETF holdings, info, country/sector weightings, kline (OHLCV), and fund flow.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Path prefix and endpoints

- **Prefix**: `/api/v1/etf/`
- **Paths** (all GET):
  - `holdings` — ETF holdings (top constituents)
  - `info` — ETF basic information
  - `country-weightings` — allocation by country
  - `sector-weightings` — allocation by sector
  - `kline` — ETF OHLCV candlestick data
  - `fund-flow` — ETF fund flow data

## Parameters by endpoint

### ETF Info (`/api/v1/etf/info`)

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | ETF symbol (uppercase, e.g., SPY, QQQ, IWM) |

**Response fields** (in `data` object):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Ticker symbol, the unique identifier for the ETF listed on an exchange |
| `name` | string | The official full name of the fund |
| `description` | string | A summary of the ETF's investment objective, tracked index, and key features |
| `logo` | string | URL to the ETF logo image |
| `isin` | string | International Securities Identification Number; a unique code for identifying securities globally |
| `assetClass` | string | The primary category of assets the ETF invests in (e.g., "Equity") |
| `securityCusip` | string | A unique alphanumeric code used to identify securities, primarily in North America |
| `domicile` | string | The country or jurisdiction where the fund is legally registered (e.g., "US") |
| `website` | string | The URL link to the product's official detail page |
| `etfCompany` | string | The fund family or company managing the ETF (e.g., "SPDR") |
| `expenseRatio` | float64 | The annual fee charged to investors to manage the fund (e.g., 0.0945 means 0.0945%) |
| `assetsUnderManagement` | float64 | The total market value of the financial assets managed by the fund |
| `avgVolume` | int64 | The average number of shares traded daily over a specific period |
| `inceptionDate` | string | The date when the fund was launched and began trading |
| `nav` | float64 | Net Asset Value per share of the ETF |
| `navCurrency` | string | The currency in which the NAV is denominated (e.g., "USD") |
| `holdingsCount` | int32 | The total number of individual securities held in the ETF portfolio |
| `updatedAt` | string | Timestamp indicating when this data entry was last refreshed |
| `sectorsList` | array | Sector breakdown list showing how the fund's assets are distributed across industries |
| `sectorsList[].industry` | string | The specific sector category (e.g., "Technology", "Financial Services") |
| `sectorsList[].exposure` | float64 | The percentage weight of this sector in the total portfolio |

---

### ETF Holdings (`/api/v1/etf/holdings`)

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | ETF symbol (uppercase, e.g., SPY, QQQ, IWM) |

**Response fields** (in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The parent ETF ticker symbol |
| `asset` | string | The ticker symbol of the held asset |
| `name` | string | Company or asset name |
| `isin` | string | International Securities Identification Number of the holding |
| `securityCusip` | string | CUSIP identifier of the holding |
| `sharesNumber` | int64 | Number of shares held |
| `weightPercentage` | float64 | Percentage weight of this holding in the portfolio |
| `marketValue` | float64 | Total market value of the holding |
| `updatedAt` | string | Last update timestamp |

Top-level response also includes `count` (int32): the number of holdings returned.

---

### ETF Country Weightings (`/api/v1/etf/country-weightings`)

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | ETF symbol (uppercase, e.g., SPY, QQQ, IWM) |

**Response fields** (in `weightings` array):

| Field | Type | Description |
|-------|------|-------------|
| `country` | string | Country name (e.g., "United States") |
| `weightPercentage` | string | Percentage weight as a string (e.g., "99.56%") |

---

### ETF Sector Weightings (`/api/v1/etf/sector-weightings`)

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | ETF symbol (uppercase, e.g., SPY, QQQ, IWM) |

**Response fields** (in `weightings` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The ETF ticker symbol |
| `sector` | string | Sector name (e.g., "Technology", "Financial Services") |
| `weightPercentage` | float64 | Percentage weight as a number (e.g., 34.62) |

---

### ETF Kline / OHLCV (`/api/v1/etf/kline`)

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | string | yes | Stock ticker symbol (e.g. AAPL, TSLA) |
| `interval` | string | yes | K-line interval. One of: `1min`, `5min`, `15min`, `30min`, `1h`, `4h`, `24h` |
| `start_time` | integer | yes | Start time (Unix timestamp, seconds, UTC) |
| `end_time` | integer | yes | End time (Unix timestamp, seconds, UTC, must be > start_time) |
| `cursor` | string | no | Pagination cursor (optional) |
| `limit` | integer | no | Maximum number of data points to return (default 100, max 5000) |

**Response fields** (in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `time_open` | int64 | K-line open time (Unix timestamp, seconds, UTC) |
| `time_close` | int64 | K-line close time (Unix timestamp, seconds, UTC) |
| `time_period_start` | string | K-line open time (RFC3339, UTC, e.g. "2024-07-24T00:00:00Z") |
| `time_period_end` | string | K-line close time (RFC3339, UTC, e.g. "2024-07-24T01:00:00Z") |
| `price_open` | float64 | Opening price |
| `price_close` | float64 | Closing price |
| `price_low` | float64 | Lowest price |
| `price_high` | float64 | Highest price |
| `trades_count` | int64 | Number of trades |
| `volume_traded` | float64 | Total traded volume |

Top-level response also includes `count` (int): number of K-lines returned, and `cursor` (string): pagination cursor for the next page (empty if no more data).

---

### ETF Fund Flow (`/api/v1/etf/fund-flow`)

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `tickers` | string | no | Comma-separated ETF tickers (e.g., SPY,QQQ,IWM) |
| `start_date` | string | no | Start date in YYYY-MM-DD format |
| `end_date` | string | no | End date in YYYY-MM-DD format |
| `as_of_start_date` | string | no | As of start date in YYYY-MM-DD format |
| `as_of_end_date` | string | no | As of end date in YYYY-MM-DD format |

**Response fields** (in `fundFlows` array):

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Flow date in ISO 8601 format |
| `ticker` | string | ETF ticker symbol |
| `sharesOutstanding` | float64 | Number of shares outstanding |
| `nav` | float64 | Net Asset Value per share |
| `flowDaily` | float64 | Daily fund flow amount (positive = inflow, negative = outflow) |
| `asOfDate` | string | Data as of date in ISO 8601 format |

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).

## Example

```js
const base = process.env.ARRAYS_API_BASE || 'https://data-gateway.prd.space.id';
const apiKey = process.env.ARRAYS_API_KEY;
const res = await fetch(`${base}/api/v1/etf/holdings?symbol=SPY`, {
  headers: { 'X-API-Key': apiKey },
});
const data = await res.json();
```
