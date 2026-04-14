# Financial statements

`GET /api/v1/stocks/company/balance-sheets`

**Timestamp Rule**: Date fields are stored in US Eastern time (ET). To include a full day's data, set `end_time` to the last second of the day in ET — e.g. for 2024-12-31: `end_time = datetime(2024, 12, 31, 23, 59, 59, tzinfo=ET).timestamp()`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase (e.g. `NVDA`, `AAPL`) |
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds). Must be > start_time |
| `period_type` | string | no | `annual` or `quarter`. Omit to return both |
| `time_type` | string | yes | `CALENDAR_END_DATE`, `FILING_DATE`, or `OBSERVED_AT` |

#### Balance sheet response fields

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Internal record ID |
| `symbol` | string | Stock symbol |
| `calendar_end_date` | string | Statement date (`YYYY-MM-DD`) |
| `fiscal_year` | string | Fiscal year |
| `period` | string | Period (`Q1`-`Q4`, `FY`) |
| `observed_at` | int64 | Observation timestamp (Unix seconds) |
| `accepted_date` | string | SEC accepted date |
| `filing_date` | string | Filing date (`YYYY-MM-DD`) |
| `reported_currency` | string | Reported currency |
| `cik` | string | CIK number |
| `cash_and_cash_equivalents` | float64 | Cash and cash equivalents |
| `short_term_investments` | float64 | Short-term investments |
| `cash_and_short_term_investments` | float64 | Cash and short-term investments |
| `net_receivables` | float64 | Net receivables |
| `accounts_receivables` | float64 | Accounts receivables |
| `other_receivables` | float64 | Other receivables |
| `inventory` | float64 | Inventory |
| `other_current_assets` | float64 | Other current assets |
| `total_current_assets` | float64 | Total current assets |
| `property_plant_equipment_net` | float64 | Property, plant and equipment (net) |
| `goodwill` | float64 | Goodwill |
| `intangible_assets` | float64 | Intangible assets |
| `goodwill_and_intangible_assets` | float64 | Goodwill and intangible assets |
| `long_term_investments` | float64 | Long-term investments |
| `tax_assets` | float64 | Tax assets |
| `other_non_current_assets` | float64 | Other non-current assets |
| `total_non_current_assets` | float64 | Total non-current assets |
| `other_assets` | float64 | Other assets |
| `total_assets` | float64 | Total assets |
| `account_payables` | float64 | Accounts payable |
| `short_term_debt` | float64 | Short-term debt |
| `tax_payables` | float64 | Tax payables |
| `deferred_revenue` | float64 | Deferred revenue |
| `other_payables` | float64 | Other payables |
| `capital_lease_obligations_current` | float64 | Current capital lease obligations |
| `other_current_liabilities` | float64 | Other current liabilities |
| `total_current_liabilities` | float64 | Total current liabilities |
| `long_term_debt` | float64 | Long-term debt |
| `deferred_revenue_non_current` | float64 | Deferred revenue (non-current) |
| `deferred_tax_liabilities_non_current` | float64 | Deferred tax liabilities (non-current) |
| `other_non_current_liabilities` | float64 | Other non-current liabilities |
| `total_non_current_liabilities` | float64 | Total non-current liabilities |
| `other_liabilities` | float64 | Other liabilities |
| `capital_lease_obligations` | float64 | Capital lease obligations |
| `total_liabilities` | float64 | Total liabilities |
| `preferred_stock` | float64 | Preferred stock |
| `common_stock` | float64 | Common stock |
| `retained_earnings` | float64 | Retained earnings |
| `accumulated_other_comprehensive_income_loss` | float64 | Accumulated other comprehensive income/loss |
| `other_total_stockholders_equity` | float64 | Other total stockholders equity |
| `total_stockholders_equity` | float64 | Total stockholders equity |
| `total_equity` | float64 | Total equity |
| `total_liabilities_and_total_equity` | float64 | Total liabilities and total equity |
| `minority_interest` | float64 | Minority interest |
| `total_investments` | float64 | Total investments |
| `total_debt` | float64 | Total debt |
| `net_debt` | float64 | Net debt |
| `total_payables` | float64 | Total payables |
| `accrued_expenses` | float64 | Accrued expenses |
| `additional_paid_in_capital` | float64 | Additional paid-in capital |
| `treasury_stock` | float64 | Treasury stock |
| `prepaids` | float64 | Prepaids |
| `created_at` | string | Record creation time |
| `updated_at` | string | Record last update time |
