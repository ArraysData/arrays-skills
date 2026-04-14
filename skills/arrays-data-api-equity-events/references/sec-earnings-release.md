# Sec Earnings Release

`GET /api/v1/stocks/sec-earnings-release`

Retrieve the SEC earnings release publication date and filing URL for a company's official earnings report, filed with the SEC for a specific fiscal period.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, IBM) |
| `period_type` | string | Yes | `annual` or `quarterly` |
| `fiscal_year` | integer | Yes | Fiscal year (e.g., 2024) |
| `fiscal_quarter` | string | No | Fiscal quarter: `Q1`, `Q2`, `Q3`, `Q4` — required when period_type is `quarterly` |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `quarter` | string | Fiscal period identifier (e.g., "202401" = fiscal year 2024, Q1) |
| `release_date` | string | SEC publication date (YYYY-MM-DD) |
| `url` | string | URL to the SEC filing document |

---
