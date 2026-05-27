# Company detail

`GET /api/v1/stocks/company/detail`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | no | Stock symbol, uppercase (e.g. `AAPL`) |
| `name` | string | no | Company name keyword (case-insensitive) |

At least one of `symbol` or `name` should be provided.

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `name` | string | Company name |
| `cik` | string | CIK number (SEC identifier) |
| `sector` | string | Industry sector |
| `industry` | string | Sub-industry |
| `exchange` | string | Exchange name |
| `exchange_short_name` | string | Exchange short name (e.g. `NASDAQ`) |
| `employees` | int32 | Number of employees |
| `ipo_date` | string | IPO date (`YYYY-MM-DD`) |
| `is_listed` | bool | Is actively listed/traded |
| `is_etf` | bool | Is ETF |
| `is_adr` | bool | Is ADR |
| `is_fund` | bool | Is fund |
| `revenue` | float64 | Annual revenue |
| `net_income` | float64 | Annual net income |
| `eps` | float64 | Earnings per share |
| `market_cap` | float64 | Market capitalization |
| `pe_ratio` | float64 | Price-to-earnings ratio |
| `ps_ratio` | float64 | Price-to-sales ratio |
| `pb_ratio` | float64 | Price-to-book ratio |
| `dividend_yield` | float64 | Dividend yield |
| `enterprise_value` | float64 | Enterprise value |
| `ev_ebitda` | float64 | EV/EBITDA ratio |
| `roe` | float64 | Return on equity |
| `debt_to_assets` | float64 | Debt-to-assets ratio |
| `price` | float64 | Current stock price |
| `logo` | string | Company logo URL |
| `company_description` | string | Company description |
| `website` | string | Company website URL |
| `country` | string | Country/region |
| `ceo` | string | CEO name |
