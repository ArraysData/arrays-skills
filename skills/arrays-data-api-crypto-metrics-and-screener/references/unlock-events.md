# Unlock events

`GET /api/v1/crypto/unlock-events`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token_id` | string | yes | Token identifier (e.g. `arbitrum`, `optimism`, `sui`) |
| `start` | string | no | Start date (`YYYY-MM-DD`) |
| `end` | string | no | End date (`YYYY-MM-DD`) |

**Response fields** — the top-level response body contains:

| Field | Type | Description |
|-------|------|-------------|
| `metadata` | object | Query metadata |
| `metadata.query_date` | string | ISO 8601 date of the query |
| `status` | boolean | API status |
| `data` | array | Array of unlock event objects |

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `unlock_date` | string | ISO 8601 date of the unlock event |
| `token_name` | string | Full token name (e.g. `"Arbitrum"`) |
| `token_symbol` | string | Token symbol (e.g. `"ARB"`) |
| `listed_method` | string | Listing method (e.g. `"INTERNAL"`) |
| `data_source` | string | Data source (e.g. `"Whitepaper"`) |
| `linear_unlocks` | object or null | Linear unlock data (null if not applicable) |
| `cliff_unlocks` | object or null | Cliff unlock data (null if not applicable) |
| `latest_update_date` | string | When the data was last updated |

`cliff_unlocks` object:

| Field | Type | Description |
|-------|------|-------------|
| `cliff_amount` | float64 | Total cliff token amount |
| `cliff_value` | float64 | Total cliff value in USD |
| `value_to_market_cap` | float64 | Percentage of market cap |
| `allocation_breakdown` | array | Breakdown by allocation |

`linear_unlocks` object:

| Field | Type | Description |
|-------|------|-------------|
| `linear_amount` | float64 | Total linear token amount |
| `linear_value` | float64 | Total linear value in USD |
| `value_to_market_cap` | float64 | Percentage of market cap |
| `allocation_breakdown` | array | Breakdown by allocation |

Each item in `allocation_breakdown`:

| Field | Type | Description |
|-------|------|-------------|
| `unlock_date` | string | ISO 8601 date |
| `allocation_name` | string | Name of allocation (e.g. `"Investors"`) |
| `standard_allocation_name` | string | Standardized name (e.g. `"Private Investors"`) |
| `cliff_amount` | float64 | Token amount in this allocation |
| `cliff_value` | float64 | Value in USD |
| `reference_price` | float64 | Reference price used for calculation |
| `reference_price_updated_time` | string | When reference price was updated |
| `unlock_precision` | string | Precision of unlock (e.g. `"MONTH"`, `"DAY"`) |
