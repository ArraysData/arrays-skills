# SEC filings

`GET /api/v1/stocks/sec-filings`

10-K and 10-Q filing metadata for US SEC registrants, newest first, with a link to the EDGAR document. Coverage from 2010. Foreign private issuers (20-F / 40-F filers such as `TSM`) return an empty array; dotted non-US symbols are rejected.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | US stock symbol (`AAPL`) |
| `form_type` | string | no | `10-K` or `10-Q` |
| `fiscal_year` | int | no | Fiscal year (`2026`) |
| `fiscal_quarter` | string | no | `Q1`, `Q2`, `Q3`, `Q4`, or `FY`; requires `fiscal_year` |
| `limit` | int | no | Max rows (1–500; default all) |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `cik` | string | SEC Central Index Key, zero-padded to 10 digits |
| `accession_number` | string | EDGAR accession number (`0000320193-26-000020`) |
| `form_type` | string | `10-K` or `10-Q` |
| `filing_date` | string | Date filed with the SEC (`YYYY-MM-DD`) |
| `report_date` | string | Period end date the filing reports on (`YYYY-MM-DD`) |
| `acceptance_time` | int64 | EDGAR acceptance instant (Unix seconds) |
| `fiscal_year` | int32 | Issuer fiscal year |
| `fiscal_quarter` | string | `Q1`–`Q4` for 10-Q, `FY` for 10-K; omitted when not derivable |
| `file_url` | string | EDGAR URL of the primary document |
