# Congress Recent Trades

`GET /api/v1/stocks/congress/recent-trades`

Retrieve stock trades made by US senators and representatives. `start_time`, `end_time` and `time_type` are always required — a call without them returns HTTP 400 `VALIDATION_ERROR`, not the latest disclosures. The optional filters (`symbol`, `name`, `tag`, `transaction_type`) combine as AND: passing `symbol` and `name` together returns only that politician's trades in that symbol.

#### Request parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | No | Politician name (partial match, case-insensitive) |
| `symbol` | string | No | Stock symbol |
| `tag` | string | No | Chamber filter: `senate`, `house`, `all` (default: `all`; case-sensitive) |
| `transaction_type` | string | No | Transaction type filter: `Buy`, `Sell`, `Exchange` (case-sensitive) |
| `start_time` | integer | Yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | Yes | End time (Unix timestamp in seconds) |
| `time_type` | string | Yes | Filter time type: `TRANSACTION_DATE`, `FILING_DATE`, or `OBSERVED_AT` |
| `limit` | integer | No | Maximum results (1-1000, default: 100). `0` is treated as unset (default 100 applies); negative or >1000 returns 400 |

There is no pagination — `offset`/`page`/`cursor` are ignored, and the response
carries no `pagination` object. A window is capped at `limit` (max 1000) and
excess rows are dropped silently. When `len(data) == limit`, split the time range
and re-query; busy months exceed 1000 rows. The window is inclusive at both ends,
so use non-overlapping split boundaries, or dedupe on
`(transaction_date, politician_id, symbol, transaction_type, amounts)` after
merging — records carry no unique id. Invalid `tag`/`time_type` values return
HTTP 400 `VALIDATION_ERROR`; invalid `transaction_type` returns HTTP 200 with an
empty `data` array.

#### Response

```json
{
  "success": true,
  "data": [
    {
      "name": "Tommy Tuberville",
      "official_name": "Tommy Tuberville",
      "symbol": "ORCL",
      "transaction_type": "Sell",
      "amounts": "$15,001 - $50,000",
      "transaction_date": "2025-10-07",
      "filing_date": "2025-11-15",
      "member_type": "senate",
      "party": "republican",
      "state": "AL",
      ...
    }
  ]
}
```

Each element in `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Politician's common name |
| `official_name` | string | Politician's name as filed. May be absent |
| `symbol` | string | Stock symbol |
| `issuer` | string | Issuer name |
| `is_active` | boolean | Whether the politician is currently in office |
| `politician_id` | string | Politician identifier |
| `reporter` | string | Reporter name |
| `party` | string | Party: `democrat`, `republican`, `independent`, `libertarian`. May be absent |
| `state` | string | Two-letter state code. May be absent |
| `transaction_type` | string | Transaction type: `Buy`, `Sell`, or `Exchange` |
| `amounts` | string | Trade amount in USD — a range (e.g., "$1,001 - $15,000") or an exact value (e.g., "$616") |
| `notes` | string | Additional disclosure notes |
| `transaction_date` | string | Date of actual trade |
| `filing_date` | string | Date of disclosure filing |
| `member_type` | string | Chamber: `senate` or `house` |
| `observed_at` | int64 | Observed timestamp (Unix seconds) |

Range bounds in `amounts` are not normalized — both `$1,000 - $15,000` and
`$1,001 - $15,000` occur. Match ranges by upper bound, not exact string.
