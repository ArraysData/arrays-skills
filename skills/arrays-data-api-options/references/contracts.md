# Option Contracts

`GET /api/v1/options/contracts`

Get options contract specifications and metadata. Returns standardized contract details such as exercise style, expiration dates, strike prices, and shares per contract.

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Underlying symbol (e.g. `SPY`, `AAPL`) |
| `options_ticker` | string | no | Exact options contract ticker match |
| `is_expired` | string | no | Expiration filter: `false` (default), `true`, or `all` |
| `contract_type` | string | no | Contract type: `call` or `put` |
| `expiration_date_min` | string | no | Min expiration date (`YYYY-MM-DD`) |
| `expiration_date_max` | string | no | Max expiration date (`YYYY-MM-DD`) |
| `strike_price_min` | number | no | Min strike price |
| `strike_price_max` | number | no | Max strike price |
| `exercise_style` | string | no | Exercise style: `american` or `european` |
| `sort_by` | string | no | Sort field: `expiration_date`, `strike_price`, or `options_ticker` |
| `sort_order` | string | no | Sort direction: `asc` or `desc` |
| `cursor` | string | no | Pagination cursor |
| `limit` | int | no | Results per page (default 100, max 1000) |

## Response

```json
{
  "success": true,
  "data": [
    {
      "options_ticker": "O:AAPL260401C00180000",
      "underlying_symbol": "AAPL",
      "contract_type": "call",
      "exercise_style": "american",
      "expiration_date": "2026-04-01",
      "strike_price": 180,
      "shares_per_contract": 100,
      "primary_exchange": "BATO",
      "cfi": "OCASPS",
      "is_expired": false
    }
  ],
  "pagination": { "limit": 0, "cursor": "...", "has_more": true },
  "request_id": "..."
}
```

**Each item in `data` (OptionsContractData):**

| Field | Type | Description |
|-------|------|-------------|
| `options_ticker` | string | OCC-format ticker with `O:` prefix (e.g. `O:AAPL260410C00200000`) |
| `underlying_symbol` | string | Underlying stock ticker |
| `contract_type` | string | `call` or `put` |
| `exercise_style` | string | `american` or `european` |
| `expiration_date` | string | Expiration date (`YYYY-MM-DD`) |
| `strike_price` | number | Strike price |
| `shares_per_contract` | integer | Shares per contract (typically 100) |
| `primary_exchange` | string | Primary listing exchange |
| `cfi` | string | CFI classification code |
| `is_expired` | boolean | Whether the contract has expired |

---
