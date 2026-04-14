# Price target consensus

`GET /api/v1/stocks/company/price-target-consensus`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (uppercase, e.g., META, AAPL) |

**Response fields** (single object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `target_high` | float64 | Highest analyst price target |
| `target_low` | float64 | Lowest analyst price target |
| `target_consensus` | float64 | Consensus (average) analyst price target |
| `target_median` | float64 | Median analyst price target |
