# Financial metrics

`GET /api/v1/stocks/financial-metrics`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `metric` | string | yes | Metric type (see list below) |
| `symbol` | string | no | Stock symbol (if omitted, returns all stocks) |
| `start_time` | int64 | yes | Start time (Unix seconds) — filters by `observed_at` (see note below) |
| `end_time` | int64 | yes | End time (Unix seconds) — filters by `observed_at` (see note below) |

**`observed_at` and date ranges**: `start_time`/`end_time` filter by `observed_at`, which is the **data publication date** (earnings release), NOT the fiscal period end date. Publication typically happens 1–3 months after the fiscal period closes. Fiscal years also don't always align with the calendar year (e.g. Apple's FY starts in October, Nike's in June). To reliably capture all quarters for a given fiscal year, use a wide date range — e.g. set `start_time` 6 months before the fiscal year and `end_time` 6 months after, then filter results by `fiscal_year` and `period`.

**Metric types**: `REVENUE_TTM`, `NET_INCOME_TTM`, `EPS_TTM`, `ROE_TTM`, `ROA_TTM`, `ROIC_TTM`, `GROSS_MARGIN_MRQ`, `OPERATING_MARGIN_MRQ`, `NET_MARGIN_MRQ`, `FCF_MARGIN_MRQ`, `RD_TO_SALES_TTM`, `DEBT_TO_EQUITY_MRQ`, `DEBT_TO_ASSETS_MRQ`, `CURRENT_RATIO_MRQ`, `QUICK_RATIO_MRQ`, `NET_WORKING_CAPITAL_MRQ`, `REVENUE_GROWTH_QOQ`, `REVENUE_GROWTH_YOY_QUARTERLY`, `REVENUE_GROWTH_YOY_TTM`, `REVENUE_GROWTH_YOY_ANNUAL`, `EPS_GROWTH_QOQ`, `EPS_GROWTH_YOY_QUARTERLY`, `EPS_GROWTH_YOY_TTM`, `EPS_GROWTH_YOY_ANNUAL`, `FCF_GROWTH_QOQ`, `FCF_GROWTH_YOY_QUARTERLY`, `FCF_GROWTH_YOY_TTM`, `FCF_GROWTH_YOY_ANNUAL`

**Response fields** (each item in `data` array is a `SymbolMetricData`):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol (e.g. `AAPL`) |
| `metric` | string | Metric type identifier (e.g. `REVENUE_TTM`) |
| `values` | array | Time series data points |

Each entry in `values`:

| Field | Type | Description |
|-------|------|-------------|
| `observed_at` | int64 | Observation timestamp (Unix seconds) |
| `value` | float64 | Metric value (null if NaN/Inf) |
| `period` | string | Fiscal period (`Q1`-`Q4`, `FY`) |
| `fiscal_year` | string | Fiscal year (e.g. `2024`) |
