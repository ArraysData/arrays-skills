# Ratings

`GET /api/v1/stocks/ratings`

Get Point-in-Time (PIT) stock ratings data for a specific symbol within a time range.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (e.g., AAPL, TSLA) |
| `start_time` | integer | yes | Start timestamp (Unix seconds, UTC) |
| `end_time` | integer | yes | End timestamp (Unix seconds, UTC) |
| `limit` | integer | no | Maximum number of results (1-1000, default: 50) |

**Response fields** (in `data` array — each element is a `PITStockRatingData`):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | Rating date (YYYY-MM-DD format) |
| `rating` | string | Overall rating (e.g., "A+", "B", "C") |
| `overall_score` | int32 | Overall composite score |
| `discounted_cash_flow_score` | int32 | DCF model score |
| `return_on_equity_score` | int32 | ROE score |
| `return_on_assets_score` | int32 | ROA score |
| `debt_to_equity_score` | int32 | Debt-to-Equity ratio score |
| `price_to_earnings_score` | int32 | P/E ratio score |
| `price_to_book_score` | int32 | P/B ratio score |
| `publish_time` | int64 | Data publish timestamp (Unix seconds, UTC) |
