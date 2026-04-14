# Ipo Calendar

`GET /api/v1/stocks/ipo-calendar`

Upcoming IPO schedules with company details, expected pricing, and market information.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from` | string | No | Start date in YYYY-MM-DD format (e.g., 2025-04-24) |
| `to` | string | No | End date in YYYY-MM-DD format (e.g., 2025-07-24) |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | IPO date (YYYY-MM-DD) |
| `daa` | string | IPO date-time (ISO 8601) |
| `company` | string | Company name |
| `exchange` | string | Exchange (e.g., "NYSE") |
| `actions` | string | Status (e.g., "Expected") |
| `shares` | integer | Number of shares offered (may be null) |
| `price_range` | string | Expected price range (may be null) |
| `market_cap` | string | Expected market cap (may be null) |

---
