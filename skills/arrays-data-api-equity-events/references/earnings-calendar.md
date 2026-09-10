# Earnings Calendar

`GET /api/v1/stocks/earnings-calendar`

Earnings calendar data with optional filtering by symbol and/or date range.

**Coverage**: US major-exchange listings, from **2025-01-01** to roughly **30 days ahead of the query date**. Past rows are kept once the report is filed, so the endpoint answers "when did X report". A future row exists only when a confirmed date falls inside that ~30-day window — most symbols have none at any given time, so `data[0]` is usually the latest *past* report; check its `date` before treating it as the next scheduled one. Non-US symbols are legacy backfill frozen at 2025-08-12: they appear only in all-symbol range queries, and a dotted-suffix `symbol` returns `400 INVALID_PARAMETER`. For the reported figures, use `arrays-data-api-equity-fundamentals`.

**Use this endpoint for event dates only — not financial figures.** `earnings-calendar` reports *when* a company reports, not the reported numbers. For actual or estimated EPS and revenue, go to the financials/estimates endpoints, which are the authoritative, consistently-scoped source:
- **Actual EPS / revenue** → `arrays-data-api-equity-fundamentals` (`company/income-statements`: `eps`, `eps_diluted`, `revenue`).
- **Estimated EPS / revenue** → `arrays-data-api-equity-estimates-and-targets` (`estimates-guidance` with `metrics=EPS,SALES` — analyst consensus).

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | No | Stock symbol (e.g., AAPL, MSFT) - optional |
| `start_time` | integer | No | Start timestamp (Unix seconds, int64 UTC) - optional, requires end_time |
| `end_time` | integer | No | End timestamp (Unix seconds, int64 UTC) - optional, requires start_time |
| `limit` | integer | No | Page size (1-1000, default: 1000); `0` or >1000 returns 400 |
| `offset` | integer | No | Rows to skip before the page (min 0, default: 0) |
| `sort_order` | string | No | `asc` or `desc` by `date` (default: `desc`); lowercase only, any other value returns 400 |

> **Sort order:** newest-first for every call shape; pass `sort_order=asc` for
> oldest-first.

**Paging**: one response carries at most `limit` records, so a wide all-symbol
range is cut at the oldest end. Page with `offset`; `pagination` echoes the
`limit`/`offset` in effect but carries no total, so treat exactly `limit` records
as "there may be more".

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
