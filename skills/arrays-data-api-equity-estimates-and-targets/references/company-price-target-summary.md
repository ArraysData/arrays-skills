# Price target summary

`GET /api/v1/stocks/company/price-target-summary`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (uppercase, e.g., META, AAPL) |

**Response fields** (single object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `last_month_count` | int32 | Number of analyst targets in the last month |
| `last_month_avg_price_target` | float64 | Average price target over the last month |
| `last_quarter_count` | int32 | Number of analyst targets in the last quarter |
| `last_quarter_avg_price_target` | float64 | Average price target over the last quarter |
| `last_year_count` | int32 | Number of analyst targets in the last year |
| `last_year_avg_price_target` | float64 | Average price target over the last year |
| `all_time_count` | int32 | Total number of analyst targets (all time) |
| `all_time_avg_price_target` | float64 | Average price target (all time) |
| `publishers` | string | Comma-separated list of publisher names |
