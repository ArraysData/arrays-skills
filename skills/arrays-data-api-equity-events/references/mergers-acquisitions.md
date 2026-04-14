# Mergers Acquisitions

`GET /api/v1/stocks/mergers-acquisitions`

Mergers and acquisitions events filtered by date range and/or symbol.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from` | string | No | Start date (YYYY-MM-DD, e.g., 2023-08-10) |
| `to` | string | No | End date (YYYY-MM-DD, e.g., 2023-08-11) |
| `symbol` | string | No | Stock symbol (e.g., AAPL, RIO, WLKP) |

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
