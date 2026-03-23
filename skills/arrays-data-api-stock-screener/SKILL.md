---
name: arrays-data-api-stock-screener
description: Calls Arrays REST APIs for stock screening and filtering — company screener with 70+ filters (sector, valuation, financials, ownership, events), basic-info screener by country/exchange/industry/sector, event screener (IPO/splits/earnings), and financial/technical metrics screener. Use when the user wants to find, filter, or screen stocks by any criteria.
---

# Arrays Data API — Stock Screener

Company screener, basic-info screener (by country, exchange, industry, sector), event screener, financial metrics screener, and technical metrics screener.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Endpoints

All under prefix `/api/v1/stocks/` (all GET):

| Path | Description |
|------|-------------|
| `company/screener` | General company screener (70+ filter params) |
| `basic-info-screener/country` | Stocks by country |
| `basic-info-screener/exchange` | Stocks by exchange |
| `basic-info-screener/industry` | Stocks by industry |
| `basic-info-screener/sector` | Stocks by sector |
| `event-screener` | Stocks by corporate events |
| `screener/financial-metrics` | Financial metrics screener (snapshot) |
| `screener/technical-metrics` | Technical metrics screener (snapshot) |
| `screener/financial-metrics/timerange` | Financial metrics screener (time range) |
| `screener/technical-metrics/timerange` | Technical metrics screener (time range) |

## Parameters by endpoint

### Company screener (`company/screener`)

The most powerful endpoint with 70+ optional filters. Key parameter groups:

**Pagination & sorting** (most commonly used):

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `offset` | int | yes | Pagination offset (>=0, default 0) |
| `limit` | int | yes | Page size (1-100, default 10) |
| `sort_by` | string | no | Sort field: `employees`, `market_cap`, `pe_ratio`, `ps_ratio`, `pb_ratio`, `ipo_date`, `price_change`, `total_volume`, `price` (default `market_cap`) |
| `sort_desc` | string | no | `asc` or `desc` (default `asc`) |

**Market filters**:

| Param | Type | Description |
|-------|------|-------------|
| `interval` | string | Aggregation interval: `5m`, `15m`, `30m`, `1h`, `4h`, `1d`, `7d`, `30d` |
| `price_min` / `price_max` | number | Price range |
| `price_change_min` / `price_change_max` | number | Price change range |
| `volume_min` / `volume_max` | number | Volume range |
| `market_cap_min` / `market_cap_max` | number | Market cap range |

**Classification filters**:

| Param | Type | Description |
|-------|------|-------------|
| `sector` | string | GICS sector: `Basic Materials`, `Communication Services`, `Consumer Cyclical`, `Consumer Defensive`, `Energy`, `Financial Services`, `Healthcare`, `Industrials`, `Real Estate`, `Technology`, `Utilities` |
| `industry` | string | Sub-industry (e.g. `Semiconductors`, `Software - Application`) |
| `exchange` | string | `NASDAQ`, `NYSE`, `OTC`, etc. |
| `country` | string | ISO country code (e.g. `US`, `CN`, `JP`) |
| `is_active_trading` / `is_etf` / `is_adr` / `is_fund` | bool | Type filters |

**Valuation filters** (all min/max pairs):
`pe_ratio`, `ps_ratio`, `pb_ratio`, `div_yield`, `ev_ebitda`, `ev`, `roe`, `debt_to_assets`

**Financial filters** (all min/max pairs):
`revenue`, `net_income`, `eps`, `gross_profit_ratio`, `operating_profit_ratio`

**Ownership filters** (all min/max pairs):
`total_invested_change`, `investors_holding`, `ownership_percent`, `insider_buy_count`, `insider_sell_count`

**Event date filters** (all start/end pairs, YYYY-MM-DD):
`recent_split_calendar`, `upcoming_split_calendar`, `recent_earnings_date`, `upcoming_earnings_date`, `recent_equity_offerings_date`

**Response fields** (each item in `data.list`):

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Stock ticker symbol (e.g. `AAPL`) |
| `company_name` | string | Full company name (e.g. `Apple Inc.`) |
| `logo` | string | URL to company logo image |
| `sector` | string | GICS sector name |
| `industry` | string | Industry name |
| `exchange_short_name` | string | Short exchange name (e.g. `NASDAQ`) |
| `cik` | string | SEC CIK number (e.g. `0000320193`) |
| `website` | string | Company website URL |
| `ceo` | string | CEO name |
| `exchange` | string | Full exchange name |
| `country` | string | Country of incorporation |
| `employees` | integer | Number of employees |
| `ipo_date` | string | IPO date (`YYYY-MM-DD`) |
| `is_active_trading` | boolean | Whether actively trading |
| `is_etf` | boolean | Whether the listing is an ETF |
| `is_adr` | boolean | Whether the listing is an ADR |
| `is_fund` | boolean | Whether the listing is a fund |
| `revenue` | number | Revenue from latest filings |
| `net_income` | number | Net income from latest filings |
| `eps` | number | Earnings per share |
| `dividend_yield` | number | Dividend yield |
| `enterprise_value` | number | Enterprise value |
| `enterprise_value_over_ebitda` | number | EV/EBITDA ratio |
| `roe` | number | Return on equity |
| `debt_to_assets` | number | Debt-to-assets ratio |
| `market_cap` | number | Market capitalization |
| `open_price` | number | Open price for the interval |
| `close_price` | number | Close/last price for the interval |
| `high_price` | number | Highest price during the interval |
| `low_price` | number | Lowest price during the interval |
| `total_volume` | number | Total trading volume during the interval |
| `total_trades_count` | number | Total number of trades during the interval |
| `price_change` | number | Absolute price change during the interval |
| `consensus` | string | Analyst consensus label |
| `overall_score` | number | Analyst overall score |
| `total_invested_change` | number | Total invested change by institutions |
| `institutional_investors_holding` | number | Number of institutional investors holding |
| `institutional_ownership_percent` | number | Institutional ownership percentage |
| `pe_ratio` | number | Price-to-earnings ratio |
| `ps_ratio` | number | Price-to-sales ratio |
| `pb_ratio` | number | Price-to-book ratio |
| `recent_split_calendar` | string | Most recent stock split date |
| `upcoming_split_calendar` | string | Next upcoming stock split date |
| `recent_earnings_date` | string | Most recent earnings date |
| `upcoming_earnings_date` | string | Next upcoming earnings date |
| `recent_ipo_date` | string | Recent IPO date |
| `upcoming_ipo_date` | string | Upcoming IPO date |
| `recent_equity_offerings_date` | string | Recent equity offerings date |
| `insider_buy_count` | integer | Number of insider buy transactions |
| `insider_sell_count` | integer | Number of insider sell transactions |
| `congressional_transaction_date` | string | Congressional trade transaction date |
| `gross_profit_ratio` | number | Gross profit margin ratio |
| `operating_profit_ratio` | number | Operating profit margin ratio |

The top-level response also contains `data.total` (integer) -- the total number of matching records for pagination.

### Basic-info screener endpoints

Each takes a single required parameter:

| Endpoint | Param | Values |
|----------|-------|--------|
| `basic-info-screener/country` | `country` | ISO alpha-2 codes: `US`, `CN`, `JP`, `GB`, `DE`, etc. |
| `basic-info-screener/exchange` | `exchange` | `AMEX`, `NASDAQ`, `NYSE` |
| `basic-info-screener/sector` | `sector` | Same GICS sectors as company screener |
| `basic-info-screener/industry` | `industry` | e.g. `Semiconductors`, `Banks Regional`, `Software Application` |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `type` | string | Screener dimension used: `sector`, `industry`, `country`, or `exchange` |
| `value` | string | The value that was matched (e.g. `Technology`, `US`, `NASDAQ`) |

### Event screener (`event-screener`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `event_type` | string | yes | `IPO Date`, `Split Date`, or `Earnings Date` |
| `start_time` | string | yes | Start date (`YYYY-MM-DD`) |
| `end_time` | string | yes | End date (`YYYY-MM-DD`). For Split/Earnings, max 1 year range. |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `type` | string | Event type matched (e.g. `IPO Date`, `Split Date`, `Earnings Date`) |
| `value` | string | The event date or related value |

### Financial/technical metrics screener (`screener/financial-metrics`, `screener/technical-metrics`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `snapshot` | int | yes | Snapshot time (Unix seconds) |
| `metric_type` | string | yes | Metric type (see lists below) |
| `range_min` | float64 | no | Min value filter |
| `range_max` | float64 | no | Max value filter |
| `order_by` | string | no | `ASC` or `DESC` (default `DESC`) |

**Financial metric types**: `REVENUE_TTM`, `NET_INCOME_TTM`, `EPS_TTM`, `ROE_TTM`, `ROA_TTM`, `ROIC_TTM`, `GROSS_MARGIN_MRQ`, `OPERATING_MARGIN_MRQ`, `NET_MARGIN_MRQ`, `FCF_MARGIN_MRQ`, `CURRENT_RATIO_MRQ`, `DEBT_TO_EQUITY_MRQ`, `DEBT_TO_ASSETS_MRQ`, `NET_WORKING_CAPITAL_MRQ`, `QUICK_RATIO_MRQ`, `RD_TO_SALES_TTM`, `MARKET_CAP`, `PE_RATIO`, `PS_RATIO`, `PB_RATIO`, `DIVIDEND_YIELD`, `ENTERPRISE_VALUE`, `EV_EBITDA_RATIO`, and growth metrics (`REVENUE_GROWTH_QOQ`, `REVENUE_GROWTH_YOY_QUARTERLY`, `REVENUE_GROWTH_YOY_TTM`, `REVENUE_GROWTH_YOY_ANNUAL`, `EPS_GROWTH_QOQ`, `EPS_GROWTH_YOY_QUARTERLY`, `EPS_GROWTH_YOY_TTM`, `EPS_GROWTH_YOY_ANNUAL`, `FCF_GROWTH_QOQ`, `FCF_GROWTH_YOY_QUARTERLY`, `FCF_GROWTH_YOY_TTM`, `FCF_GROWTH_YOY_ANNUAL`)

**Technical metric types**: `PRICE_CHANGE_1D/1W/1M/3M/6M/YTD/1Y/3Y/5Y`, `SHARES_VOLUME`, `DOLLAR_VOLUME`, `AVERAGE_DAILY_DOLLAR_VOLUME`, `MA_5/10/20/60/120/200`, `EMA_5/10/20/60/120/200`, `RSI_14`, `MACD_DIF/DEA/HIST`, `BOLLINGER_UPPER/MID/LOWER`, `VWAP_DAY`, `BETA`, `VOLATILITY_20/60/90`

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `snapshotTime` | integer | Snapshot time as Unix timestamp in seconds (UTC) |
| `date` | string | Snapshot date in `YYYY-MM-DD` format |
| `metric` | string | Metric type that was queried (e.g. `PE_RATIO`, `MA_5`) |
| `value` | number | Metric value for this stock |

### Time range variants (`screener/financial-metrics/timerange`, `screener/technical-metrics/timerange`)

Same as snapshot variants but replace `snapshot` with:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | int | yes | Start (Unix seconds) |
| `end_time` | int | yes | End (Unix seconds) |
| `limit` | int | no | Max results per day |

**Response fields** (each item in `data` array is a date group):

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date in `YYYY-MM-DD` format |
| `items` | array | Array of stock metric data for this date |

Each object in the `items` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `snapshotTime` | integer | Snapshot time as Unix timestamp in seconds (UTC) |
| `metric` | string | Metric type that was queried (e.g. `PE_RATIO`, `MA_5`) |
| `value` | number | Metric value for this stock |

## Response format

**V2** (all screener endpoints):
```json
{ "success": true, "data": { "list": [...], "total": 100 }, "request_id": "..." }
```

Basic-info screener and metrics screener return:
```json
{ "success": true, "data": [...], "request_id": "..." }
```

**Error**:
```json
{ "success": false, "error": { "code": "...", "message": "..." }, "request_id": "..." }
```

## Pagination

`company/screener` uses offset-based pagination: set `offset` and `limit`, check `total` in response.

## Example

```js
const base = process.env.ARRAYS_API_BASE || 'https://data-gateway.prd.space.id';
const apiKey = process.env.ARRAYS_API_KEY;
if (!apiKey) throw new Error('ARRAYS_API_KEY is not set');

// Screen for Technology stocks with PE < 20, sorted by market cap
const res = await fetch(
  `${base}/api/v1/stocks/company/screener?sector=Technology&pe_ratio_max=20&sort_by=market_cap&sort_desc=desc&offset=0&limit=20`,
  { headers: { 'X-API-Key': apiKey } }
);
const json = await res.json();
if (!json.success) throw new Error(json.error?.message || 'API error');
const stocks = json.data.list; // Array of stock objects
const total = json.data.total;
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
