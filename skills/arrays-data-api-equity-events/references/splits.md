# Splits

`GET /api/v1/stocks/splits`

PIT (Point-in-Time) stock split data for a specific symbol within a time range.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, TSLA, NVDA) |
| `start_time` | integer | Yes | Start timestamp (Unix seconds, UTC) |
| `end_time` | integer | Yes | End timestamp (Unix seconds, UTC) |
| `limit` | integer | No | Maximum number of results (1-1000, default: 50) |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | Split date (YYYY-MM-DD) |
| `numerator` | number | Split numerator (e.g., 2.0 for a 2-for-1 split) |
| `denominator` | number | Split denominator (e.g., 1.0 for a 2-for-1 split) |

---
