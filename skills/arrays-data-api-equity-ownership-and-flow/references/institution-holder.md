# Institution Holder

`GET /api/v1/stocks/institution-holder`

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
      "calendar_end_date": "2024-06-30",
      "investor_name": "VANGUARD GROUP INC",
      "symbol": "AAPL",
      "shares_number": 1255256,
      "market_value": 26850000,
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
| `calendar_end_date` | string | Date of the holding record |
| `cik` | string | CIK identifier |
| `filing_date` | string | Filing date |
| `investor_name` | string | Name of the institutional investor |
| `symbol` | string | Stock symbol |
| `security_name` | string | Security name |
| `type_of_security` | string | Type of security |
| `security_cusip` | string | Security CUSIP |
| `shares_type` | string | Shares type |
| `put_call_share` | string | Put/Call/Share indicator |
| `investment_discretion` | string | Investment discretion type |
| `industry_title` | string | Industry title |
| `weight` | float64 | Portfolio weight |
| `last_weight` | float64 | Previous portfolio weight |
| `change_in_weight` | float64 | Change in weight |
| `change_in_weight_percentage` | float64 | Change in weight percentage |
| `market_value` | float64 | Market value |
| `last_market_value` | float64 | Previous market value |
| `change_in_market_value` | float64 | Change in market value |
| `change_in_market_value_percentage` | float64 | Change in market value percentage |
| `shares_number` | int64 | Number of shares held |
| `last_shares_number` | int64 | Previous number of shares held |
| `change_in_shares_number` | int64 | Change in shares number |
| `change_in_shares_number_percentage` | float64 | Change in shares number percentage |
| `quarter_end_price` | float64 | Quarter end price |
| `avg_price_paid` | float64 | Average price paid |
| `is_new` | bool | Whether this is a new position |
| `is_sold_out` | bool | Whether position was sold out |
| `ownership` | float64 | Ownership percentage |
| `last_ownership` | float64 | Previous ownership percentage |
| `change_in_ownership` | float64 | Change in ownership |
| `change_in_ownership_percentage` | float64 | Change in ownership percentage |
| `holding_period` | int32 | Holding period in quarters |
| `first_added` | string | First added date |
| `performance` | int64 | Performance value |
| `performance_percentage` | float64 | Performance percentage |
| `last_performance` | int64 | Previous performance value |
| `change_in_performance` | int64 | Change in performance |
| `is_counted_for_performance` | bool | Whether counted for performance |
| `observed_at` | int64 | Observed timestamp (Unix seconds) |

---
