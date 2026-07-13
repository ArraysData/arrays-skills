# Earnings Calendar

`GET /api/v1/stocks/earnings-calendar`

Earnings calendar data with optional filtering by symbol and/or date range.

**No historical data**: `earnings-calendar` only covers upcoming/recent earnings. Past earnings entries are replaced once the actual report is filed. For historical earnings filings, use `arrays-data-api-equity-fundamentals`.

**Use this endpoint for event dates only — not financial figures.** `earnings-calendar` reports *when* a company reports, not the reported numbers. For actual or estimated EPS and revenue, go to the financials/estimates endpoints, which are the authoritative, consistently-scoped source:
- **Actual EPS / revenue** → `arrays-data-api-equity-fundamentals` (`company/income-statements`: `eps`, `eps_diluted`, `revenue`).
- **Estimated EPS / revenue** → `arrays-data-api-equity-estimates-and-targets` (`estimates-guidance` with `metrics=EPS,SALES` — analyst consensus).

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | No | Stock symbol (e.g., AAPL, MSFT) - optional |
| `start_time` | integer | No | Start timestamp (Unix seconds, int64 UTC) - optional, requires end_time |
| `end_time` | integer | No | End timestamp (Unix seconds, int64 UTC) - optional, requires start_time |

**Response**: `data[]` is a flat array of earnings calendar records. Each object in `data[]`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier |
| `symbol` | string | Stock symbol |
| `date` | string | Earnings date (YYYY-MM-DD) |
| `time` | string | Earnings call time (e.g., "amc", "bmo") |
| `fiscal_date_ending` | string | Fiscal period end date |
| `updated_from_date` | string | Date the data was updated from |
| `created_at` | string | Record creation timestamp |
| `updated_at` | string | Record last-update timestamp |

---
