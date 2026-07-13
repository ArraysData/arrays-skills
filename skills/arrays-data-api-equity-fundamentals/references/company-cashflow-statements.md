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
| `change_in_working_capital` | float64 | Change in working capital |
| `other_non_cash_items` | float64 | Other non-cash items |
| `net_cash_provided_by_operating_activities` | float64 | Net cash from operating activities |
| `acquisitions_net` | float64 | Acquisitions (net) |
| `other_investing_activities` | float64 | Other investing activities |
| `net_cash_provided_by_investing_activities` | float64 | Net cash from investing activities |
| `net_debt_issuance` | float64 | Net debt issuance |
| `net_stock_issuance` | float64 | Net stock issuance |
| `other_financing_activities` | float64 | Other financing activities |
| `net_cash_provided_by_financing_activities` | float64 | Net cash from financing activities |
| `effect_of_forex_changes_on_cash` | float64 | Effect of forex changes on cash |
| `net_change_in_cash` | float64 | Net change in cash |
| `cash_at_end_of_period` | float64 | Cash at end of period |
| `cash_at_beginning_of_period` | float64 | Cash at beginning of period |
| `operating_cash_flow` | float64 | Operating cash flow |
| `capital_expenditure` | float64 | Capital expenditure |
| `free_cash_flow` | float64 | Free cash flow |
| `net_dividends_paid` | float64 | Net dividends paid |
| `created_at` | string | Record creation time |
| `updated_at` | string | Record last update time |

#### Sign conventions

All cash flow values are signed from the company's cash position: **positive = cash in, negative = cash out**. The three activity subtotals can be either sign depending on the period:

- `net_cash_provided_by_operating_activities` / `operating_cash_flow`: positive = operations generated cash; negative = operations consumed cash.
- `net_cash_provided_by_investing_activities`: negative = **net investor** (cash spent acquiring PP&E/investments); positive = **net divestor** (cash received from selling or maturing investments).
- `net_cash_provided_by_financing_activities`: positive = net cash raised (issuance exceeds repayments); negative = net cash returned to capital providers (debt repayment, buybacks, dividends).

Pure-outflow line items are stored as negative values: `capital_expenditure`, `net_dividends_paid`. `free_cash_flow` = operating cash flow − capex.
