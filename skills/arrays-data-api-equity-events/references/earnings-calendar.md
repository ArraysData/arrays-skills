# Earnings Calendar

`GET /api/v1/stocks/earnings-calendar`

Earnings calendar data with optional filtering by symbol and/or date range.

**No historical data**: `earnings-calendar` only covers upcoming/recent earnings. Past earnings entries are replaced once the actual report is filed. For historical earnings filings, use `arrays-data-api-equity-fundamentals`.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | No | Stock symbol (e.g., AAPL, MSFT) - optional |
| `start_time` | integer | No | Start timestamp (Unix seconds, int64 UTC) - optional, requires end_time |
| `end_time` | integer | No | End timestamp (Unix seconds, int64 UTC) - optional, requires start_time |

**Response**: `data[]` is an array grouped by date. Each item has:

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Earnings date (YYYY-MM-DD) |
| `entries` | array | Array of earnings entries for that date |

Each object in `entries[]`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier |
| `symbol` | string | Stock symbol |
| `eps` | string | Actual earnings per share |
| `eps_estimated` | string | Estimated earnings per share |
| `time` | string | Earnings call time (e.g., "amc", "bmo") |
| `revenue` | string | Actual revenue |
| `revenue_estimated` | string | Estimated revenue |
| `fiscal_date_ending` | string | Fiscal period end date |
| `updated_from_date` | string | Date the data was updated from |
| `status` | string | Earnings status |
| `created_at` | string | Record creation timestamp |
| `updated_at` | string | Record last-update timestamp |

---
