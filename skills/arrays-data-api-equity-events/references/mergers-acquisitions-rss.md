# Mergers Acquisitions Rss

`GET /api/v1/stocks/mergers-acquisitions/rss`

M&A RSS feed from SEC filings with pagination.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page` | integer | No | Page number for pagination, starts from 0. If not provided, defaults to page 0 |

**Response fields** (wrapper has `count` + `data[]`; each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `company_name` | string | Acquiring company name |
| `cik` | string | Acquiring company CIK number |
| `symbol` | string | Acquiring company stock symbol |
| `targeted_company_name` | string | Target company name |
| `targeted_cik` | string | Target company CIK number |
| `targeted_symbol` | string | Target company stock symbol |
| `transaction_date` | string | Transaction date (YYYY-MM-DD) |
| `acceptance_time` | string | SEC filing acceptance time |
| `url` | string | SEC filing document URL |

---
