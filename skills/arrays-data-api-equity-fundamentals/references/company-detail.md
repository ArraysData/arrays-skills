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
| `id` | int64 | Internal record ID |
| `cik` | string | CIK number (SEC identifier) |
| `symbol` | string | Stock symbol |
| `company_name` | string | Company name |
| `logo` | string | Company logo URL |
| `website` | string | Company website URL |
| `country` | string | Country/region |
| `ceo` | string | CEO name |
| `employees` | int32 | Number of employees |
| `sector` | string | Industry sector |
| `industry` | string | Sub-industry |
| `company_description` | string | Company description |
| `ipo_date` | string | IPO date (`YYYY-MM-DD`) |
| `exchange` | string | Exchange name |
| `created_at` | string | Record creation time (ISO 8601) |
| `updated_at` | string | Record last update time (ISO 8601) |
| `is_active_trading` | bool | Is actively traded |
| `is_etf` | bool | Is ETF |
| `is_adr` | bool | Is ADR |
| `is_fund` | bool | Is fund |
