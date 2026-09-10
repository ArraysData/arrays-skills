# Ipo Confirmed Calendar

`GET /api/v1/stocks/ipo-confirmed-calendar`

Stream of **SEC registration filings** related to IPO listings. In current production data, all rows are `CERT` (certificate of registration of a class of securities — typically filed at the time of exchange listing). Each row is a filing event, keyed by `(symbol, cik, form, filing_date)`; a single company can produce multiple rows across different filing dates.

**Not a "definitive IPO list"**: despite the "confirmed" name, this endpoint does **not** return "companies that have certainly IPO'd". A row only means a registration document was filed with the SEC; the actual listing may be weeks or months later (or not at all). For the vendor's forward-looking IPO calendar with expected pricing, use `ipo-calendar`.

**Both `from` and `to` are required**: if either is missing, the response is `{"data": []}` with no error. Always pass an explicit date range.

**Historical coverage starts 2025-01-01**: no data is available prior to this date. Filter by `filing_date` (not by `effectiveness_date`).

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from` | string | Yes | Start date in YYYY-MM-DD format, on/after 2025-01-01 (e.g., 2025-01-01). Must be paired with `to`. |
| `to` | string | Yes | End date in YYYY-MM-DD format (e.g., 2025-03-31). Must be paired with `from`. |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `cik` | string | SEC CIK number |
| `form` | string | Filing form type. In current data this is always `CERT` (certificate of registration), which is filed near the listing date — so a `CERT` row is a reasonable proxy for an actual listing event |
| `filing_date` | string | Filing date (YYYY-MM-DD) — used as the range filter |
| `accepted_date` | string | Accepted date-time (YYYY-MM-DD HH:MM:SS) |
| `effectiveness_date` | string | Effectiveness date (YYYY-MM-DD) |
| `url` | string | SEC filing document URL |

---
