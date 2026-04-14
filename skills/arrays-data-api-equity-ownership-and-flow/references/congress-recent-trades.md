# Congress Recent Trades

`GET /api/v1/stocks/congress/recent-trades`

Retrieve stock trades made by US senators and representatives. Parameter priority: `symbol` > `name` > latest disclosures.

#### Request parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | No | Politician name (partial match) |
| `symbol` | string | No | Stock symbol |
| `tag` | string | No | Chamber filter: `senate`, `house`, `all` (default: `all`) |
| `transaction_type` | string | No | Transaction type filter: `Purchase`, `Sale`, `Sale (Full)`, `Sale (Partial)` |
| `start_time` | integer | Yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | Yes | End time (Unix timestamp in seconds) |
| `time_type` | string | Yes | Filter time type: `TRANSACTION_DATE`, `FILING_DATE`, or `OBSERVED_AT` |
| `limit` | integer | No | Maximum results (1-1000, default: 100) |

#### Response

```json
{
  "success": true,
  "data": [
    {
      "name": "Tommy Tuberville",
      "symbol": "ORCL",
      "transaction_type": "Sale",
      "amounts": "$15,001 - $50,000",
      "transaction_date": "2025-10-07",
      "filing_date": "2025-11-15",
      "member_type": "senate",
      ...
    }
  ]
}
```

Each element in `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Politician's full name |
| `symbol` | string | Stock symbol |
| `issuer` | string | Issuer name |
| `is_active` | boolean | Whether the politician is currently active |
| `politician_id` | string | Politician identifier |
| `reporter` | string | Reporter name |
| `transaction_type` | string | Transaction type |
| `amounts` | string | Trade amount range in USD (e.g., "$1,001 - $15,000") |
| `notes` | string | Additional disclosure notes |
| `transaction_date` | string | Date of actual trade |
| `filing_date` | string | Date of disclosure filing |
| `member_type` | string | Chamber: `senate` or `house` |
| `observed_at` | int64 | Observed timestamp (Unix seconds) |
