# Equity Offering

`GET /api/v1/stocks/equity-offering`

Latest equity offerings, including new shares being issued by companies and exempt offerings and amendments.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | integer | Yes | Page number starting from 0 |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `cik` | string | SEC CIK number |
| `url` | string | SEC filing URL |
| `company_name` | string | Company name |
| `entity_name` | string | Entity name |
| `filling_date` | string | Filing date |
| `date` | string | Offering date (ISO 8601) |
| `form_type` | string | SEC form type (e.g., "D") |
| `form_signification` | string | Form description (e.g., "Notice of Exempt Offering of Securities") |
| `issuer_street` | string | Issuer street address |
| `issuer_city` | string | Issuer city |
| `issuer_state_or_country` | string | Issuer state or country code |
| `issuer_state_or_country_description` | string | Issuer state or country full name |
| `issuer_zip_code` | string | Issuer ZIP code |
| `issuer_phone_number` | string | Issuer phone number |
| `jurisdiction_of_incorporation` | string | Jurisdiction of incorporation |
| `entity_type` | string | Entity type (e.g., "Limited Partnership") |
| `incorporated_within_five_years` | boolean | Whether incorporated within last five years |
| `year_of_incorporation` | string | Year of incorporation |
| `related_person_first_name` | string | Related person first name |
| `related_person_last_name` | string | Related person last name |
| `related_person_street` | string | Related person street address |
| `related_person_city` | string | Related person city |
| `related_person_state_or_country` | string | Related person state or country code |
| `related_person_state_or_country_description` | string | Related person state or country full name |
| `related_person_zip_code` | string | Related person ZIP code |
| `related_person_relationship` | string | Related person relationship to issuer |
| `industry_group_type` | string | Industry group type |
| `revenue_range` | string | Revenue range |
| `federal_exemptions_exclusions` | string | Federal exemptions/exclusions claimed |
| `is_amendment` | boolean | Whether this is an amendment filing |
| `date_of_first_sale` | string | Date of first sale |
| `duration_of_offering_is_more_than_year` | boolean | Whether offering duration exceeds one year |
| `securities_offered_are_of_equity_type` | boolean | Whether securities offered are equity type |
| `is_business_combination_transaction` | boolean | Whether this is a business combination |
| `minimum_investment_accepted` | integer | Minimum investment accepted (may be null) |
| `total_offering_amount` | integer | Total offering amount (may be null) |
| `total_amount_sold` | integer | Total amount sold (may be null) |
| `total_amount_remaining` | integer | Total amount remaining (may be null) |
| `has_non_accredited_investors` | boolean | Whether non-accredited investors participate |
| `total_number_already_invested` | integer | Total number already invested (may be null) |
| `sales_commissions` | integer | Sales commissions (may be null) |
| `finders_fees` | integer | Finders fees (may be null) |
| `gross_proceeds_used` | integer | Gross proceeds used (may be null) |
| `created_date` | string | Record creation date |
| `updated_date` | string | Record last-update date |
| `acceptance_time` | string | SEC filing acceptance time |

---
