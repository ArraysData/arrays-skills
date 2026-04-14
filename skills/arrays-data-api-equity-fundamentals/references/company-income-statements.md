# Financial statements

`GET /api/v1/stocks/company/income-statements`

**Timestamp Rule**: Date fields are stored in US Eastern time (ET). To include a full day's data, set `end_time` to the last second of the day in ET — e.g. for 2024-12-31: `end_time = datetime(2024, 12, 31, 23, 59, 59, tzinfo=ET).timestamp()`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase (e.g. `NVDA`, `AAPL`) |
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds). Must be > start_time |
| `period_type` | string | no | `annual` or `quarter`. Omit to return both |
| `time_type` | string | yes | `CALENDAR_END_DATE`, `FILING_DATE`, or `OBSERVED_AT` |

#### Income statement response fields

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Internal record ID |
| `symbol` | string | Stock symbol |
| `calendar_end_date` | string | Statement date (`YYYY-MM-DD`) |
| `fiscal_year` | string | Fiscal year (e.g. `2024`) |
| `period` | string | Period (`Q1`, `Q2`, `Q3`, `Q4`, `FY`) |
| `observed_at` | int64 | Observation timestamp (Unix seconds) |
| `accepted_date` | string | SEC accepted date (`YYYY-MM-DD HH:MM:SS`) |
| `filing_date` | string | Filing date (`YYYY-MM-DD`) |
| `reported_currency` | string | Reported currency (e.g. `USD`) |
| `cik` | string | CIK number |
| `revenue` | float64 | Total revenue |
| `cost_of_revenue` | float64 | Cost of revenue |
| `gross_profit` | float64 | Gross profit |
| `gross_profit_ratio` | float64 | Gross profit ratio |
| `research_and_development_expenses` | float64 | R&D expenses |
| `selling_general_and_administrative_expenses` | float64 | SG&A expenses |
| `selling_and_marketing_expenses` | float64 | Selling and marketing expenses |
| `general_and_administrative_expenses` | float64 | General and administrative expenses |
| `operating_expenses` | float64 | Total operating expenses |
| `cost_and_expenses` | float64 | Total cost and expenses |
| `interest_income` | float64 | Interest income |
| `interest_expense` | float64 | Interest expense |
| `depreciation_and_amortization` | float64 | Depreciation and amortization |
| `ebitda` | float64 | EBITDA |
| `ebitda_ratio` | float64 | EBITDA ratio |
| `operating_income` | float64 | Operating income |
| `operating_profit_ratio` | float64 | Operating profit ratio |
| `income_before_tax` | float64 | Income before tax |
| `income_tax_expense` | float64 | Income tax expense |
| `net_income` | float64 | Net income |
| `net_income_from_continuing_operations` | float64 | Net income from continuing operations |
| `net_income_from_discontinued_operations` | float64 | Net income from discontinued operations |
| `net_income_deductions` | float64 | Net income deductions |
| `ebit` | float64 | EBIT (earnings before interest and taxes) |
| `net_interest_income` | float64 | Net interest income |
| `total_other_income_expenses_net` | float64 | Total other income/expenses net |
| `non_operating_income_excluding_interest` | float64 | Non-operating income excluding interest |
| `other_expenses` | float64 | Other expenses |
| `other_adjustments_to_net_income` | float64 | Other adjustments to net income |
| `eps` | float64 | Earnings per share (basic) |
| `eps_diluted` | float64 | Earnings per share (diluted) |
| `weighted_average_shs_out` | float64 | Weighted average shares outstanding |
| `weighted_average_shs_out_dil` | float64 | Weighted average shares outstanding (diluted) |
| `net_profit_ratio` | float64 | Net profit ratio |
| `bottom_line_net_income` | float64 | Bottom line net income |
| `created_at` | string | Record creation time |
| `updated_at` | string | Record last update time |
