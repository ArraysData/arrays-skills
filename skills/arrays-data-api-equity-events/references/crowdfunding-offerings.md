# Crowdfunding — Offerings

`GET /api/v1/stocks/crowdfunding/offerings`

Paginated crowdfunding offerings information from SEC filings.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | integer | No | Page number (0-based, default: 0) |

**Response fields** (wrapper has `count` + `data[]`; each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `cik` | string | SEC CIK number |
| `company_name` | string | Company name |
| `url` | string | SEC filing URL |
| `form_type` | string | Form type (e.g., "C/A") |
| `form_signification` | string | Form description |
| `industry` | string | Industry (may be empty) |
| `filling_date` | string | Filing date |
| `date` | string | Offering date |
| `name_of_issuer` | string | Issuer name |
| `legal_status_form` | string | Legal form |
| `jurisdiction_organization` | string | Jurisdiction of organization |
| `issuer_street` | string | Issuer street address |
| `issuer_city` | string | Issuer city |
| `issuer_state_or_country` | string | Issuer state or country code |
| `issuer_zip_code` | string | Issuer ZIP code |
| `issuer_website` | string | Issuer website |
| `intermediary_company_name` | string | Intermediary company name |
| `intermediary_commission_cik` | string | Intermediary CIK number |
| `intermediary_commission_file_number` | string | Intermediary file number |
| `compensation_amount` | string | Compensation amount |
| `financial_interest` | string | Financial interest description |
| `security_offered_type` | string | Type of security offered |
| `security_offered_other_description` | string | Other security type description |
| `number_of_security_offered` | integer | Number of securities offered |
| `offering_price` | number | Offering price per security |
| `offering_amount` | number | Total offering amount |
| `over_subscription_accepted` | string | Whether over-subscription is accepted |
| `over_subscription_allocation_type` | string | Over-subscription allocation type |
| `maximum_offering_amount` | number | Maximum offering amount |
| `offering_deadline_date` | string | Offering deadline date |
| `current_number_of_employees` | number | Current employee count |
| `total_asset_most_recent_fiscal_year` | number | Total assets (most recent fiscal year) |
| `total_asset_prior_fiscal_year` | number | Total assets (prior fiscal year) |
| `cash_and_cash_equivalent_most_recent_fiscal_year` | number | Cash and equivalents (most recent fiscal year) |
| `cash_and_cash_equivalent_prior_fiscal_year` | number | Cash and equivalents (prior fiscal year) |
| `accounts_receivable_most_recent_fiscal_year` | number | Accounts receivable (most recent fiscal year) |
| `accounts_receivable_prior_fiscal_year` | number | Accounts receivable (prior fiscal year) |
| `short_term_debt_most_recent_fiscal_year` | number | Short-term debt (most recent fiscal year) |
| `short_term_debt_prior_fiscal_year` | number | Short-term debt (prior fiscal year) |
| `long_term_debt_most_recent_fiscal_year` | number | Long-term debt (most recent fiscal year) |
| `long_term_debt_prior_fiscal_year` | number | Long-term debt (prior fiscal year) |
| `revenue_most_recent_fiscal_year` | number | Revenue (most recent fiscal year) |
| `revenue_prior_fiscal_year` | number | Revenue (prior fiscal year) |
| `cost_goods_sold_most_recent_fiscal_year` | number | Cost of goods sold (most recent fiscal year) |
| `cost_goods_sold_prior_fiscal_year` | number | Cost of goods sold (prior fiscal year) |
| `taxes_paid_most_recent_fiscal_year` | number | Taxes paid (most recent fiscal year) |
| `taxes_paid_prior_fiscal_year` | number | Taxes paid (prior fiscal year) |
| `net_income_most_recent_fiscal_year` | number | Net income (most recent fiscal year) |
| `net_income_prior_fiscal_year` | number | Net income (prior fiscal year) |
| `updated_at` | string | Last update timestamp |
| `created_at` | string | Creation timestamp |
| `acceptance_time` | string | SEC filing acceptance time |
