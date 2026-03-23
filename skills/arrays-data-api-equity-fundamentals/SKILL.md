---
name: arrays-data-api-equity-fundamentals
description: Calls Arrays REST APIs for equity fundamentals — company profiles, executive compensation (salary, bonus, stock awards), income/balance/cashflow statements, financial metrics (PE, PB, ROE, EPS, margins), shares float, outstanding shares, fiscal dates, KPI, and options chain. Use when the user asks about company details, executive pay or salary, quarterly/annual financials, earnings, historical earnings filings, valuation ratios, or stock options.
---

# Arrays Data API — Equity Fundamentals

Company profiles, financial statements, shares float, outstanding shares, fiscal dates, financial metrics, KPI, and options.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Endpoints

All under prefix `/api/v1/stocks/` (all GET):

| Path | Description |
|------|-------------|
| `company/list` | Company list with filters (price, volume, sector, financials) |
| `company/detail` | Company profile |
| `company/income-statements` | Income statements by time range |
| `company/balance-statements` | Balance sheet by time range |
| `company/cashflow-statements` | Cash flow by time range |
| `company/executives_info` | Company executives info |
| `company/kpi` | KPI values by fiscal period |
| `financial-metrics` | Financial metrics time series (PE, ROE, EPS, margins, etc.) |
| `shares-float` | Shares float |
| `outstanding-shares` | Outstanding shares over time |
| `fiscal-dates` | Fiscal period dates |
| `fiscal-dates-by-range` | Fiscal dates by date range |
| `options/list` | Options chain |

## CRITICAL: Fiscal and Calendar Quarter Mapping

Many companies have fiscal years that do NOT align with the calendar year.

**Default**: When there is no FY/CY qualifier (e.g., "what was AAPL's 20xx Qx earning?") → treat as **fiscal quarter**. Treat as calendar quarter only when the user says "Calendar Year", "CY", gives a specific month/date or gives an explicit range (e.g., "Jul 2025", "CY 2025", "as of March 2025", "Jan-Mar 2025"). To get company financials, when faced with a calendar quarter/year, first determine which fiscal quarter/year it corresponds to. **Never assume fiscal = calendar.**

**FY → CY** (what calendar dates does a fiscal quarter cover?):
- Call `fiscal-dates` with `fiscal_year` + `fiscal_quarter` → use `calendarEnd` as the period end date.

**CY → FY** (which fiscal quarter does a calendar period fall in?):
- Call `fiscal-dates-by-range` with the calendar date range → returns `fiscalYear` + `fiscalQuarter`.

**Earnings announcement vs. filing date**:
- Full financials (statements) are typically filed **1 day after** the press earnings release / earnings call.
- When the question mentions "announcement date", "release date", or "publish date", add **1–2 days buffer** to look up the fiscal period.

**Quarterly vs. yearly results**:
- **For cash flow / income / balance statements**: When looking for quarterly results, remember to filter the returned `data` array to match the exact `period` (e.g., `Q2`) and `fiscalYear`, and exclude `FY` entries.

**`time_type` selection**:
- `CALENDAR_END_DATE` — filter by the calendar end date of the financial reporting period.
- `FILING_DATE` — filter by when the report was officially filed/published with the SEC (e.g., "reports filed in 2024", "filed on Feb 6"). Note: filing date is typically 1–2 days after the earnings release.
- `OBSERVED_AT` — filter by point-in-time data availability.

## Parameters by endpoint

### Company list (`company/list`)

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interval` | string | no | Time interval: `5min`, `15min`, `30min`, `1h`, `4h`, `24h`, `7d`, `30d` |
| `min_price` | float64 | no | Minimum price |
| `max_price` | float64 | no | Maximum price |
| `min_price_change` | float64 | no | Minimum price change |
| `max_price_change` | float64 | no | Maximum price change |
| `min_volume` | int64 | no | Minimum volume |
| `max_volume` | int64 | no | Maximum volume |
| `min_market_cap` | float64 | no | Minimum market capitalization |
| `max_market_cap` | float64 | no | Maximum market capitalization |
| `symbol` | string | no | Stock symbol, uppercase (e.g. `AAPL`) |
| `cik` | string | no | CIK code |
| `sector` | string | no | Sector (e.g. `Technology`, `Healthcare`, `Financial Services`) |
| `industry` | string | no | Sub-industry (e.g. `Semiconductors`, `Consumer Electronics`) |
| `exchange` | string | no | Exchange name |
| `exchange_short_name` | string | no | Exchange short name |
| `country` | string | no | Country/region |
| `is_active_trading` | bool | no | Is actively traded |
| `is_etf` | bool | no | Is ETF |
| `is_adr` | bool | no | Is ADR |
| `is_fund` | bool | no | Is fund |
| `min_employees` | int32 | no | Minimum number of employees |
| `max_employees` | int32 | no | Maximum number of employees |
| `ipo_start` | string | no | IPO start date (`YYYY-MM-DD`) |
| `ipo_end` | string | no | IPO end date (`YYYY-MM-DD`) |
| `rev_min` | float64 | no | Minimum revenue |
| `rev_max` | float64 | no | Maximum revenue |
| `ni_min` | float64 | no | Minimum net income |
| `ni_max` | float64 | no | Maximum net income |
| `eps_min` | float64 | no | Minimum earnings per share |
| `eps_max` | float64 | no | Maximum earnings per share |
| `gm_min` | float64 | no | Minimum gross margin (%) |
| `gm_max` | float64 | no | Maximum gross margin (%) |
| `opm_min` | float64 | no | Minimum operating profit margin (%) |
| `opm_max` | float64 | no | Maximum operating profit margin (%) |
| `pe_min` | float64 | no | Minimum P/E ratio |
| `pe_max` | float64 | no | Maximum P/E ratio |
| `ps_min` | float64 | no | Minimum P/S ratio |
| `ps_max` | float64 | no | Maximum P/S ratio |
| `pb_min` | float64 | no | Minimum P/B ratio |
| `pb_max` | float64 | no | Maximum P/B ratio |
| `div_yield_min` | float64 | no | Minimum dividend yield (%) |
| `div_yield_max` | float64 | no | Maximum dividend yield (%) |
| `ev_ebitda_min` | float64 | no | Minimum EV/EBITDA |
| `ev_ebitda_max` | float64 | no | Maximum EV/EBITDA |
| `ev_min` | float64 | no | Minimum enterprise value |
| `ev_max` | float64 | no | Maximum enterprise value |
| `roe_min` | float64 | no | Minimum return on equity (%) |
| `roe_max` | float64 | no | Maximum return on equity (%) |
| `dta_min` | float64 | no | Minimum debt-to-assets ratio (%) |
| `dta_max` | float64 | no | Maximum debt-to-assets ratio (%) |
| `offset` | int32 | no | Pagination offset (default 0) |
| `limit` | int32 | no | Items per page (default 10, max 100) |
| `sort_by` | string | no | Sort field: `employees`, `price_change`, `total_volume`, `price`, `market_cap` |
| `sort_desc` | string | no | Sort direction: `asc` or `desc` |

**Response fields** (each item in `response` array):

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Stock symbol (e.g. `AAPL`) |
| `name` | string | Company name |
| `logo` | string | Company logo URL |
| `sector` | string | Industry sector |
| `industry` | string | Sub-industry |
| `exchange` | string | Exchange name |
| `country` | string | Country/region |
| `employees` | int32 | Number of employees |
| `ipo_date` | string | IPO date (`YYYY-MM-DD`) |
| `is_active_trading` | bool | Is actively traded |
| `is_etf` | bool | Is ETF |
| `is_adr` | bool | Is ADR |
| `is_fund` | bool | Is fund |
| `created_at` | int64 | Created timestamp (Unix seconds) |
| `revenue` | float64 | Revenue (USD) |
| `net_income` | float64 | Net income (USD) |
| `eps` | float64 | Earnings per share |
| `gross_profit_margin` | float64 | Gross profit margin (%) |
| `operating_profit_margin` | float64 | Operating profit margin (%) |
| `pe_ratio` | float64 | Price-to-earnings ratio |
| `ps_ratio` | float64 | Price-to-sales ratio |
| `pb_ratio` | float64 | Price-to-book ratio |
| `dividend_yield` | float64 | Dividend yield (%) |
| `ev_ebitda` | float64 | Enterprise value / EBITDA |
| `roe` | float64 | Return on equity (%) |
| `debt_to_assets` | float64 | Debt-to-assets ratio |
| `market_cap` | float64 | Market capitalization (USD) |
| `open_price` | float64 | Open price |
| `close_price` | float64 | Close price |
| `high_price` | float64 | High price |
| `low_price` | float64 | Low price |
| `total_volume` | int64 | Total volume |
| `total_trades_count` | int64 | Total trades count |
| `price_change` | float64 | Price change |

Top-level response also includes `total` (int32) for total count.

### Company detail (`company/detail`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | no | Stock symbol, uppercase (e.g. `AAPL`) |
| `name` | string | no | Company name keyword (case-insensitive) |

At least one of `symbol` or `name` should be provided.

**Response fields** (each item in `response` array):

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Internal record ID |
| `cik` | string | CIK number (SEC identifier) |
| `ticker` | string | Stock symbol |
| `companyName` | string | Company name |
| `logo` | string | Company logo URL |
| `website` | string | Company website URL |
| `country` | string | Country/region |
| `ceo` | string | CEO name |
| `employees` | int32 | Number of employees |
| `sector` | string | Industry sector |
| `industry` | string | Sub-industry |
| `companyDescription` | string | Company description |
| `ipoDate` | string | IPO date (`YYYY-MM-DD`) |
| `exchange` | string | Exchange name |
| `createdAt` | string | Record creation time (ISO 8601) |
| `updatedAt` | string | Record last update time (ISO 8601) |
| `isActiveTrading` | bool | Is actively traded |
| `isEtf` | bool | Is ETF |
| `isAdr` | bool | Is ADR |
| `isFund` | bool | Is fund |

### Financial statements (`company/income-statements`, `company/balance-statements`, `company/cashflow-statements`)

**Timestamp Rule**: Date fields are stored in US Eastern time (ET). To include a full day's data, set `end_time` to the first second of the next day in ET — e.g. for 2024-12-31: `end_time = datetime(2025, 1, 1, 0, 0, 0, tzinfo=ET).timestamp()`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase (e.g. `NVDA`, `AAPL`) |
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds). Must be > start_time |
| `period_type` | string | no | `annual` or `quarter`. Omit to return both |
| `time_type` | string | yes | `CALENDAR_END_DATE`, `FILING_DATE`, or `OBSERVED_AT` |

#### Income statement response fields (`company/income-statements`)

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Internal record ID |
| `symbol` | string | Stock symbol |
| `calendarEndDate` | string | Statement date (`YYYY-MM-DD`) |
| `fiscalYear` | string | Fiscal year (e.g. `2024`) |
| `period` | string | Period (`Q1`, `Q2`, `Q3`, `Q4`, `FY`) |
| `observedAt` | int64 | Observation timestamp (Unix seconds) |
| `acceptedDate` | string | SEC accepted date (`YYYY-MM-DD HH:MM:SS`) |
| `filingDate` | string | Filing date (`YYYY-MM-DD`) |
| `reportedCurrency` | string | Reported currency (e.g. `USD`) |
| `cik` | string | CIK number |
| `revenue` | float64 | Total revenue |
| `costOfRevenue` | float64 | Cost of revenue |
| `grossProfit` | float64 | Gross profit |
| `grossProfitRatio` | float64 | Gross profit ratio |
| `researchAndDevelopmentExpenses` | float64 | R&D expenses |
| `sellingGeneralAndAdministrativeExpenses` | float64 | SG&A expenses |
| `sellingAndMarketingExpenses` | float64 | Selling and marketing expenses |
| `generalAndAdministrativeExpenses` | float64 | General and administrative expenses |
| `operatingExpenses` | float64 | Total operating expenses |
| `costAndExpenses` | float64 | Total cost and expenses |
| `interestIncome` | float64 | Interest income |
| `interestExpense` | float64 | Interest expense |
| `depreciationAndAmortization` | float64 | Depreciation and amortization |
| `ebitda` | float64 | EBITDA |
| `ebitdaRatio` | float64 | EBITDA ratio |
| `operatingIncome` | float64 | Operating income |
| `operatingProfitRatio` | float64 | Operating profit ratio |
| `incomeBeforeTax` | float64 | Income before tax |
| `incomeTaxExpense` | float64 | Income tax expense |
| `netIncome` | float64 | Net income |
| `netIncomeFromContinuingOperations` | float64 | Net income from continuing operations |
| `netIncomeFromDiscontinuedOperations` | float64 | Net income from discontinued operations |
| `netIncomeDeductions` | float64 | Net income deductions |
| `ebit` | float64 | EBIT (earnings before interest and taxes) |
| `netInterestIncome` | float64 | Net interest income |
| `totalOtherIncomeExpensesNet` | float64 | Total other income/expenses net |
| `nonOperatingIncomeExcludingInterest` | float64 | Non-operating income excluding interest |
| `otherExpenses` | float64 | Other expenses |
| `otherAdjustmentsToNetIncome` | float64 | Other adjustments to net income |
| `eps` | float64 | Earnings per share (basic) |
| `epsDiluted` | float64 | Earnings per share (diluted) |
| `weightedAverageShsOut` | float64 | Weighted average shares outstanding |
| `weightedAverageShsOutDil` | float64 | Weighted average shares outstanding (diluted) |
| `netProfitRatio` | float64 | Net profit ratio |
| `bottomLineNetIncome` | float64 | Bottom line net income |
| `createdAt` | string | Record creation time |
| `updatedAt` | string | Record last update time |

#### Balance sheet response fields (`company/balance-statements`)

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Internal record ID |
| `symbol` | string | Stock symbol |
| `calendarEndDate` | string | Statement date (`YYYY-MM-DD`) |
| `fiscalYear` | string | Fiscal year |
| `period` | string | Period (`Q1`-`Q4`, `FY`) |
| `observedAt` | int64 | Observation timestamp (Unix seconds) |
| `acceptedDate` | string | SEC accepted date |
| `filingDate` | string | Filing date (`YYYY-MM-DD`) |
| `reportedCurrency` | string | Reported currency |
| `cik` | string | CIK number |
| `cashAndCashEquivalents` | float64 | Cash and cash equivalents |
| `shortTermInvestments` | float64 | Short-term investments |
| `cashAndShortTermInvestments` | float64 | Cash and short-term investments |
| `netReceivables` | float64 | Net receivables |
| `accountsReceivables` | float64 | Accounts receivables |
| `otherReceivables` | float64 | Other receivables |
| `inventory` | float64 | Inventory |
| `otherCurrentAssets` | float64 | Other current assets |
| `totalCurrentAssets` | float64 | Total current assets |
| `propertyPlantEquipmentNet` | float64 | Property, plant and equipment (net) |
| `goodwill` | float64 | Goodwill |
| `intangibleAssets` | float64 | Intangible assets |
| `goodwillAndIntangibleAssets` | float64 | Goodwill and intangible assets |
| `longTermInvestments` | float64 | Long-term investments |
| `taxAssets` | float64 | Tax assets |
| `otherNonCurrentAssets` | float64 | Other non-current assets |
| `totalNonCurrentAssets` | float64 | Total non-current assets |
| `otherAssets` | float64 | Other assets |
| `totalAssets` | float64 | Total assets |
| `accountPayables` | float64 | Accounts payable |
| `shortTermDebt` | float64 | Short-term debt |
| `taxPayables` | float64 | Tax payables |
| `deferredRevenue` | float64 | Deferred revenue |
| `otherPayables` | float64 | Other payables |
| `capitalLeaseObligationsCurrent` | float64 | Current capital lease obligations |
| `otherCurrentLiabilities` | float64 | Other current liabilities |
| `totalCurrentLiabilities` | float64 | Total current liabilities |
| `longTermDebt` | float64 | Long-term debt |
| `deferredRevenueNonCurrent` | float64 | Deferred revenue (non-current) |
| `deferredTaxLiabilitiesNonCurrent` | float64 | Deferred tax liabilities (non-current) |
| `otherNonCurrentLiabilities` | float64 | Other non-current liabilities |
| `totalNonCurrentLiabilities` | float64 | Total non-current liabilities |
| `otherLiabilities` | float64 | Other liabilities |
| `capitalLeaseObligations` | float64 | Capital lease obligations |
| `totalLiabilities` | float64 | Total liabilities |
| `preferredStock` | float64 | Preferred stock |
| `commonStock` | float64 | Common stock |
| `retainedEarnings` | float64 | Retained earnings |
| `accumulatedOtherComprehensiveIncomeLoss` | float64 | Accumulated other comprehensive income/loss |
| `otherTotalStockholdersEquity` | float64 | Other total stockholders equity |
| `totalStockholdersEquity` | float64 | Total stockholders equity |
| `totalEquity` | float64 | Total equity |
| `totalLiabilitiesAndTotalEquity` | float64 | Total liabilities and total equity |
| `minorityInterest` | float64 | Minority interest |
| `totalInvestments` | float64 | Total investments |
| `totalDebt` | float64 | Total debt |
| `netDebt` | float64 | Net debt |
| `totalPayables` | float64 | Total payables |
| `accruedExpenses` | float64 | Accrued expenses |
| `additionalPaidInCapital` | float64 | Additional paid-in capital |
| `treasuryStock` | float64 | Treasury stock |
| `prepaids` | float64 | Prepaids |
| `createdAt` | string | Record creation time |
| `updatedAt` | string | Record last update time |

#### Cash flow statement response fields (`company/cashflow-statements`)

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Internal record ID |
| `symbol` | string | Stock symbol |
| `calendarEndDate` | string | Statement date (`YYYY-MM-DD`) |
| `fiscalYear` | string | Fiscal year |
| `period` | string | Period (`Q1`-`Q4`, `FY`) |
| `observedAt` | int64 | Observation timestamp (Unix seconds) |
| `acceptedDate` | string | SEC accepted date |
| `filingDate` | string | Filing date (`YYYY-MM-DD`) |
| `reportedCurrency` | string | Reported currency |
| `cik` | string | CIK number |
| `netIncome` | float64 | Net income |
| `depreciationAndAmortization` | float64 | Depreciation and amortization |
| `deferredIncomeTax` | float64 | Deferred income tax |
| `stockBasedCompensation` | float64 | Stock-based compensation |
| `changeInWorkingCapital` | float64 | Change in working capital |
| `accountsReceivables` | float64 | Accounts receivables change |
| `inventory` | float64 | Inventory change |
| `accountsPayables` | float64 | Accounts payables change |
| `otherWorkingCapital` | float64 | Other working capital |
| `otherNonCashItems` | float64 | Other non-cash items |
| `netCashProvidedByOperatingActivities` | float64 | Net cash from operating activities |
| `investmentsInPropertyPlantAndEquipment` | float64 | Investments in PP&E |
| `acquisitionsNet` | float64 | Acquisitions (net) |
| `purchasesOfInvestments` | float64 | Purchases of investments |
| `salesMaturitiesOfInvestments` | float64 | Sales/maturities of investments |
| `otherInvestingActivities` | float64 | Other investing activities |
| `netCashProvidedByInvestingActivities` | float64 | Net cash from investing activities |
| `debtRepayment` | float64 | Debt repayment |
| `commonStockIssuance` | float64 | Common stock issued |
| `commonStockRepurchased` | float64 | Common stock repurchased |
| `commonDividendsPaid` | float64 | Common dividends paid |
| `preferredDividendsPaid` | float64 | Preferred dividends paid |
| `otherFinancingActivities` | float64 | Other financing activities |
| `netCashProvidedByFinancingActivities` | float64 | Net cash from financing activities |
| `effectOfForexChangesOnCash` | float64 | Effect of forex changes on cash |
| `netChangeInCash` | float64 | Net change in cash |
| `cashAtEndOfPeriod` | float64 | Cash at end of period |
| `cashAtBeginningOfPeriod` | float64 | Cash at beginning of period |
| `operatingCashFlow` | float64 | Operating cash flow |
| `capitalExpenditure` | float64 | Capital expenditure |
| `freeCashFlow` | float64 | Free cash flow |
| `netDebtIssuance` | float64 | Net debt issuance |
| `longTermNetDebtIssuance` | float64 | Long-term net debt issuance |
| `shortTermNetDebtIssuance` | float64 | Short-term net debt issuance |
| `netStockIssuance` | float64 | Net stock issuance |
| `netCommonStockIssuance` | float64 | Net common stock issuance |
| `netPreferredStockIssuance` | float64 | Net preferred stock issuance |
| `netDividendsPaid` | float64 | Net dividends paid |
| `incomeTaxesPaid` | float64 | Income taxes paid |
| `interestPaid` | float64 | Interest paid |
| `createdAt` | string | Record creation time |
| `updatedAt` | string | Record last update time |

### Executives info (`company/executives_info`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase (e.g. `META`, `AAPL`) |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `cik` | string | CIK number |
| `symbol` | string | Stock symbol |
| `company_name` | string | Company name |
| `filing_date` | string | Filing date (`YYYY-MM-DD`) |
| `accepted_date` | string | SEC accepted date (`YYYY-MM-DD HH:MM:SS`) |
| `name_and_position` | string | Executive name and position |
| `year` | int64 | Compensation year |
| `salary` | int64 | Base salary |
| `bonus` | int64 | Bonus (may be null) |
| `stock_award` | int64 | Stock awards (may be null) |
| `option_award` | int64 | Option awards (may be null) |
| `incentive_plan_compensation` | int64 | Incentive plan compensation (may be null) |
| `all_other_compensation` | int64 | All other compensation (may be null) |
| `total` | int64 | Total compensation (may be null) |
| `link` | string | SEC filing link |

### KPI (`company/kpi`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase |
| `fiscal_year` | int | yes | Fiscal year (e.g. `2024`) |
| `fiscal_quarter` | string | yes | `Q1`, `Q2`, `Q3`, `Q4`, or `FY` (for annual) |

**IMPORTANT**: KPI metric names vary by company. A metric value of `0` or `null` may indicate a name mismatch, not actual zero. When searching for a specific KPI:
- First retrieve all metrics without filtering, then match by partial case-insensitive string matching on the `name` field.
- **When looking for revenue**, prioritize metrics ending with `_revenue` (e.g., `sams_club_revenue`, `linkedin_revenue`) over metrics containing "sales" (which may match growth rates like `comparable_sales_growth`). Match `_revenue` first, then fall back to broader matching.
- For segment revenue (e.g., Home Depot's "Building Materials"), look for the closest matching metric name.

**KPI metric name matching**: When searching for a category's total revenue (e.g., "building materials revenue"), **always prefer the metric with `total_` prefix** (e.g., `total_building_materials_revenue`) over the base name (e.g., `building_materials_revenue`). The base-name metric is often a sub-component that may be zero, while the `total_` variant is the correct aggregate. Pattern:
```python
# Find the right metric — prefer total_ prefix
target = "building_materials"
best = None
for m in all_metrics:
    name = m["name"].lower()
    if f"total_{target}_revenue" == name:
        best = m
        break  # exact total match — done
    if target in name and "revenue" in name and not best:
        best = m  # fallback
print(best["value"] if best else "API_ERROR: metric not found")
```

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `periodType` | string | Period type (`annual`, `quarterly`) |
| `periodId` | string | Unique period identifier |
| `calendarEndDate` | string | Report date (`YYYY-MM-DD`) |
| `calendarYear` | int32 | Calendar year |
| `calendarQuarter` | string | Calendar quarter (`Q1`-`Q4`) |
| `fiscalYear` | int32 | Fiscal year |
| `fiscalQuarter` | string | Fiscal quarter (`Q1`-`Q4`) |
| `values` | object | KPI metrics as key-value pairs, where key is the metric name (e.g. `total_building_materials_revenue`, `us_revenue`) and value is the metric value |

### Financial metrics (`financial-metrics`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `metric` | string | yes | Metric type (see list below) |
| `symbol` | string | no | Stock symbol (if omitted, returns all stocks) |
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds) |

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
| `observedAt` | int64 | Observation timestamp (Unix seconds) |
| `value` | float64 | Metric value (null if NaN/Inf) |
| `period` | string | Fiscal period (`Q1`-`Q4`, `FY`) |
| `fiscalYear` | string | Fiscal year (e.g. `2024`) |

### Shares float (`shares-float`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase |

**Response fields** (each item in `response` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | Data date and time |
| `freeFloat` | float64 | Free float percentage |
| `floatShares` | string | Number of float shares |
| `outstandingShares` | string | Number of outstanding shares |
| `source` | string | Data source URL (SEC filing link) |

### Outstanding shares (`outstanding-shares`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol |
| `period` | string | yes | `quarterly` or `annual` (default `quarterly`) |
| `start_time` | int64 | yes | Unix seconds |
| `end_time` | int64 | yes | Unix seconds |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Stock symbol |
| `description` | string | Description text |
| `date` | string | Date |
| `period` | string | Period type |
| `fiscalYear` | string | Fiscal year |
| `fiscalQuarter` | string | Fiscal quarter |
| `totalOutstanding` | float64 | Total outstanding shares |
| `unit` | string | Unit of measurement |
| `adrDescription` | string | ADR description (may be null) |
| `adrRatio` | float64 | ADR ratio (may be null) |
| `adrFsymId` | string | ADR FactSet symbol ID (may be null) |
| `adrTotalOutstanding` | float64 | ADR total outstanding (may be null) |

### Fiscal dates (`fiscal-dates`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | string | yes | Stock symbol |
| `fiscal_year` | int | yes | Fiscal year (e.g. `2024`) |
| `fiscal_quarter` | string | yes | `Q1`, `Q2`, `Q3`, `Q4`, or `FY` |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Stock symbol |
| `fiscalYear` | int32 | Fiscal year |
| `fiscalQuarter` | string | Fiscal quarter (`Q1`-`Q4`, `FY`) |
| `calendarEnd` | string | End date of the fiscal period (`YYYY-MM-DD`) |
| `publicDate` | string | Date earnings report was publicly released (`YYYY-MM-DD`), empty if not available |

### Fiscal dates by range (`fiscal-dates-by-range`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | string | yes | Stock symbol |
| `start_time` | string | yes | Start date (`YYYY-MM-DD`), matches by `calendarEnd` (NOT `publicDate`) |
| `end_time` | string | yes | End date (`YYYY-MM-DD`), matches by `calendarEnd` (NOT `publicDate`) |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Stock symbol |
| `fiscalYear` | int32 | Fiscal year |
| `fiscalQuarter` | string | Fiscal quarter (`Q1`-`Q4`, `FY`) |
| `calendarEnd` | string | End date of the fiscal period (`YYYY-MM-DD`) |
| `publicDate` | string | Date earnings report was publicly released (`YYYY-MM-DD`), empty if not available |

### Options chain (`options/list`)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `stock_ticker` | string | yes | Stock ticker, uppercase |
| `option_ticker` | string | no | Filter by specific option ticker |
| `start_expiration_date` | int64 | no | Start expiration (Unix seconds) |
| `end_expiration_date` | int64 | no | End expiration (Unix seconds) |
| `contract_type` | string | no | `put` or `call` |
| `min_strike_price` | float64 | no | Min strike price |
| `max_strike_price` | float64 | no | Max strike price |
| `cursor` | string | no | Pagination cursor |
| `limit` | int64 | yes | Max results (1-1000) |

**Response fields:**

Top-level:

| Field | Type | Description |
|-------|------|-------------|
| `results` | array | Array of option contract details |
| `cursor` | string | Pagination cursor for next page (empty if no more results) |

Each item in `results` (OptionContractDetail):

| Field | Type | Description |
|-------|------|-------------|
| `break_even_price` | float64 | Break-even price |
| `daily_data` | object | Daily price data (see below) |
| `details` | object | Contract specifications (see below) |
| `greeks` | object | Option Greeks (see below) |
| `implied_volatility` | float64 | Implied volatility |
| `open_interest` | int32 | Open interest |
| `underlying_asset` | object | Underlying stock info (see below) |
| `fmv` | float64 | Fair market value |

`daily_data` fields:

| Field | Type | Description |
|-------|------|-------------|
| `change` | float64 | Price change |
| `change_percent` | float64 | Price change percentage |
| `close` | float64 | Close price |
| `high` | float64 | High price |
| `last_updated` | int64 | Last updated timestamp (Unix seconds) |
| `low` | float64 | Low price |
| `open` | float64 | Open price |
| `previous_close` | float64 | Previous close price |

`details` fields:

| Field | Type | Description |
|-------|------|-------------|
| `contract_type` | string | Contract type (`call` or `put`) |
| `exercise_style` | string | Exercise style (e.g. `american`) |
| `expiration_date` | string | Expiration date |
| `shares_per_contract` | int32 | Shares per contract (typically 100) |
| `strike_price` | float64 | Strike price |
| `ticker` | string | Option ticker symbol |

`greeks` fields:

| Field | Type | Description |
|-------|------|-------------|
| `delta` | float64 | Delta |
| `gamma` | float64 | Gamma |
| `theta` | float64 | Theta |
| `vega` | float64 | Vega |

`underlying_asset` fields:

| Field | Type | Description |
|-------|------|-------------|
| `change_to_break_even` | float64 | Change to break even |
| `last_updated` | int64 | Last updated timestamp (Unix seconds) |
| `price` | float64 | Current underlying price |
| `ticker` | string | Underlying stock ticker |
| `timeframe` | string | Timeframe (e.g. `1d`) |

## Response format

Endpoints use **two different** response wrappers:

**Standard format** (company/detail, company/list, shares-float) — data in `response` field:
```json
{ "success": true, "response": [ ... ], "total": 42 }
```
Access in Python: `body["response"]`

**Standard nested format** (executives_info, outstanding-shares) — data in `response.data`:
```json
{ "success": true, "response": { "data": [ ... ], "total": 42 } }
```
Access in Python: `body["response"]["data"]`

**V2 format** (income-statements, balance-statements, cashflow-statements, financial-metrics, kpi, fiscal-dates, fiscal-dates-by-range) — data in `data` field:
```json
{ "success": true, "data": [ ... ] }
```
Access in Python: `body["data"]`

## Pagination

- `company/list`: Use `offset` (default 0) + `limit` (default 10, max 100). Check `total` in response.
- `options/list`: Cursor-based. Pass `cursor` from previous response's pagination info.

## Python examples

```python
import requests, os
from datetime import datetime
from zoneinfo import ZoneInfo
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

ET = ZoneInfo("America/New_York")
def to_ts(y, m, d): return int(datetime(y, m, d, tzinfo=ET).timestamp())

# Income statements (V2 — use body["data"])
resp = requests.get(f"{base}/api/v1/stocks/company/income-statements",
    params={"symbol": "AAPL", "start_time": to_ts(2024, 1, 1), "end_time": to_ts(2025, 1, 1),
            "period_type": "quarter"},
    headers={"X-API-Key": key})
body = resp.json()
statements = body["data"]  # flat array of income statement objects
for s in statements:
    print(f"Revenue: {s['revenue']}, Net Income: {s['netIncome']}")

# KPI values (V2 — use body["data"])
resp = requests.get(f"{base}/api/v1/stocks/company/kpi",
    params={"symbol": "HD", "fiscal_year": 2025, "fiscal_quarter": "Q3"},
    headers={"X-API-Key": key})
body = resp.json()
kpis = body["data"]  # flat array of KPI objects
for k in kpis:
    for name, value in k["values"].items():
        print(f"{name}: {value}")

# Company detail (Standard — use body["response"])
resp = requests.get(f"{base}/api/v1/stocks/company/detail",
    params={"symbol": "AAPL"},
    headers={"X-API-Key": key})
body = resp.json()
company = body["response"]  # single object
print(f"Name: {company['companyName']}, Sector: {company['sector']}")

# Executives info (Standard nested — use body["response"]["data"])
resp = requests.get(f"{base}/api/v1/stocks/company/executives_info",
    params={"symbol": "AAPL"},
    headers={"X-API-Key": key})
body = resp.json()
executives = body["response"]["data"]  # array of executive objects
for e in executives:
    print(f"{e['name_and_position']} ({e['year']}): salary={e['salary']}")
```
