# Financial statements

`GET /api/v1/stocks/company/cashflow-statements`

**Timestamp Rule**: Date fields are stored in US Eastern time (ET). To include a full day's data, set `end_time` to the last second of the day in ET — e.g. for 2024-12-31: `end_time = datetime(2024, 12, 31, 23, 59, 59, tzinfo=ET).timestamp()`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase (e.g. `NVDA`, `AAPL`) |
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds). Must be > start_time |
| `period_type` | string | no | `annual` or `quarter`. Omit to return both |
| `time_type` | string | yes | `CALENDAR_END_DATE`, `FILING_DATE`, or `OBSERVED_AT` |

#### Cash flow statement response fields

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
| `net_income` | float64 | Net income |
| `depreciation_and_amortization` | float64 | Depreciation and amortization |
| `deferred_income_tax` | float64 | Deferred income tax |
| `stock_based_compensation` | float64 | Stock-based compensation |
| `change_in_working_capital` | float64 | Change in working capital |
| `accounts_receivables` | float64 | Accounts receivables change |
| `inventory` | float64 | Inventory change |
| `accounts_payables` | float64 | Accounts payables change |
| `other_working_capital` | float64 | Other working capital |
| `other_non_cash_items` | float64 | Other non-cash items |
| `net_cash_provided_by_operating_activities` | float64 | Net cash from operating activities |
| `investments_in_property_plant_and_equipment` | float64 | Investments in PP&E |
| `acquisitions_net` | float64 | Acquisitions (net) |
| `purchases_of_investments` | float64 | Purchases of investments |
| `sales_maturities_of_investments` | float64 | Sales/maturities of investments |
| `other_investing_activities` | float64 | Other investing activities |
| `net_cash_provided_by_investing_activities` | float64 | Net cash from investing activities |
| `debt_repayment` | float64 | Debt repayment |
| `common_stock_issuance` | float64 | Common stock issued |
| `common_stock_repurchased` | float64 | Common stock repurchased |
| `common_dividends_paid` | float64 | Common dividends paid |
| `preferred_dividends_paid` | float64 | Preferred dividends paid |
| `other_financing_activities` | float64 | Other financing activities |
| `net_cash_provided_by_financing_activities` | float64 | Net cash from financing activities |
| `effect_of_forex_changes_on_cash` | float64 | Effect of forex changes on cash |
| `net_change_in_cash` | float64 | Net change in cash |
| `cash_at_end_of_period` | float64 | Cash at end of period |
| `cash_at_beginning_of_period` | float64 | Cash at beginning of period |
| `operating_cash_flow` | float64 | Operating cash flow |
| `capital_expenditure` | float64 | Capital expenditure |
| `free_cash_flow` | float64 | Free cash flow |
| `net_debt_issuance` | float64 | Net debt issuance |
| `long_term_net_debt_issuance` | float64 | Long-term net debt issuance |
| `short_term_net_debt_issuance` | float64 | Short-term net debt issuance |
| `net_stock_issuance` | float64 | Net stock issuance |
| `net_common_stock_issuance` | float64 | Net common stock issuance |
| `net_preferred_stock_issuance` | float64 | Net preferred stock issuance |
| `net_dividends_paid` | float64 | Net dividends paid |
| `income_taxes_paid` | float64 | Income taxes paid |
| `interest_paid` | float64 | Interest paid |
| `created_at` | string | Record creation time |
| `updated_at` | string | Record last update time |
