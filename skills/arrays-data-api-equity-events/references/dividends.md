# Dividends

`GET /api/v1/stocks/dividends`

PIT (Point-in-Time) dividend data for a specific symbol within a time range.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, MSFT, KO) |
| `start_time` | integer | Yes | Start timestamp (Unix seconds, UTC) |
| `end_time` | integer | Yes | End timestamp (Unix seconds, UTC) |
| `time_type` | string | Yes | Date type to filter by. One of: `RECORD_DATE`, `PAYMENT_DATE`, `DECLARATION_DATE` |
| `limit` | integer | No | Maximum number of results (1-1000, default: 50) |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | Ex-dividend date (YYYY-MM-DD) |
| `record_date` | string | Record date (YYYY-MM-DD) |
| `payment_date` | string | Payment date (YYYY-MM-DD) |
| `declaration_date` | string | Declaration date (YYYY-MM-DD) |
| `adj_dividend` | number | Adjusted dividend amount |
| `dividend` | number | Dividend amount |
| `yield` | number | Dividend yield percentage |
| `frequency` | string | Dividend frequency (e.g., "Quarterly", "Monthly") |

---
