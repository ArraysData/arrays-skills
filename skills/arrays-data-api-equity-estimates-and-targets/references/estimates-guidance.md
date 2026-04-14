# Estimates & guidance

`GET /api/v1/stocks/estimates-guidance`

**IMPORTANT**: This endpoint returns multiple rows for the same fiscal period, each with a different `estimate_date` (the date the consensus was computed). The most recent row by `estimate_date` may be a stale partial update with only 1 analyst — do NOT blindly use the most recent row. Instead:
- When the question asks for the estimate **on a specific date** (e.g., "on June 28th, 2025"), use `start_time` and `end_time` to get the snapshot near that date: `start_time=<unix_ts_of_date>&end_time=<unix_ts_of_next_day>`.
- When the question asks for a specific fiscal period without a date, use `fiscal_year` and `fiscal_quarter` filters and pick the row with the highest `estimate_count` (most analysts contributing).


**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (e.g., AAPL) |
| `metrics` | string | yes | Metrics (comma-separated). Supported: EPS, SALES, DPS, CFPS, EBITDA, EBIT, BPS, ASSETS |
| `type` | string | yes | Data type: `estimate` or `guidance` |
| `period_type` | string | no | Period type (default: annual). Values: `annual`, `quarterly`, `semi-annual` |
| `start_time` | integer | no | Start time for observed_at filter (Unix timestamp in seconds) |
| `end_time` | integer | no | End time for observed_at filter (Unix timestamp in seconds) |
| `fiscal_year` | integer | no | Fiscal year filter (e.g., 2024) |
| `fiscal_quarter` | string | no | Fiscal quarter filter (only valid when period_type=quarterly): `Q1`, `Q2`, `Q3`, `Q4` |
| `limit` | integer | no | Result limit (default: 10, max: 1000) |

**Response fields when `type=estimate`** (each item in `data` array is a `FactsetEstimateRow`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `fsym_id` | string | FactSet symbol ID |
| `metric` | string | Metric name (e.g., EPS, SALES, EBITDA) |
| `periodicity` | string | Period type: `annual`, `quarterly`, or `semi-annual` |
| `fiscal_period` | string | Fiscal period: `Q1`, `Q2`, `Q3`, `Q4` |
| `fiscal_year` | *int32 | Fiscal year |
| `fiscal_end_date` | string | Fiscal period end date (`YYYY-MM-DD`) |
| `estimate_date` | string | Estimate adjustment date (`YYYY-MM-DD`) |
| `observed_at` | string | Point-in-time observation timestamp (ISO 8601) |
| `mean` | *float64 | Mean estimate |
| `median` | *float64 | Median estimate |
| `standard_deviation` | *float64 | Standard deviation |
| `high` | *float64 | High estimate |
| `low` | *float64 | Low estimate |
| `estimate_count` | *int32 | Number of estimates |
| `up` | *int32 | Number of estimates increased |
| `down` | *int32 | Number of estimates decreased |

**Response fields when `type=guidance`** (each item in `data` array is a `FactsetGuidanceRow`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `fsym_id` | string | FactSet symbol ID |
| `metric` | string | Metric name (e.g., EPS, SALES, EBITDA) |
| `periodicity` | string | Period type: `annual`, `quarterly`, or `semi-annual` |
| `fiscal_period` | string | Fiscal period: `Q1`, `Q2`, `Q3`, `Q4` |
| `fiscal_year` | *int32 | Fiscal year |
| `fiscal_end_date` | string | Fiscal period end date |
| `guidance_date` | string | Guidance date (`YYYY-MM-DD`) |
| `observed_at` | string | Point-in-time observation timestamp |
| `guidance_range` | string | Guidance range string (e.g., `5.00 - 5.50`, may be omitted) |
| `guidance_low` | *float64 | Guidance low value |
| `guidance_high` | *float64 | Guidance high value |
| `guidance_midpoint` | *float64 | Guidance midpoint |
| `prev_midpoint` | *float64 | Previous guidance midpoint |
| `prev_low` | *float64 | Previous guidance low |
| `prev_high` | *float64 | Previous guidance high |
| `mean_before` | *float64 | Consensus mean before guidance |
| `mean_surprise_amt` | *float64 | Surprise amount vs mean |
| `mean_surprise_amt_ratio` | *float64 | Surprise ratio vs mean (decimal, not percentage) |
