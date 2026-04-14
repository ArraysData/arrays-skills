# Executives info

`GET /api/v1/stocks/company/executives`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase (e.g. `META`, `AAPL`) |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `cik` | string | CIK number |
| `symbol` | string | Stock symbol |
| `company_name` | string | Company name |
| `filing_date` | string | Filing date (`YYYY-MM-DD`) |
| `accepted_date` | string | SEC accepted date (`YYYY-MM-DD HH:MM:SS`) |
| `name_and_position` | string | Executive name and position |
| `year` | int64 | Compensation year |
| `salary` | int64 | Base salary |
| `bonus` | int64 | Bonus (may be null) |
| `stock_award` | int64 | Stock awards (may be null) |
| `option_award` | int64 | Option awards (may be null) |
| `incentive_plan_compensation` | int64 | Incentive plan compensation (may be null) |
| `all_other_compensation` | int64 | All other compensation (may be null) |
| `total` | int64 | Total compensation (may be null) |
| `link` | string | SEC filing link |
