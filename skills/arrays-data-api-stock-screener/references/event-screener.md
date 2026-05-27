# Event screener

`GET /api/v1/stocks/screener/events`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `event_type` | string | yes | `IPO Date`, `Split Date`, or `Earnings Date`. The API is case-insensitive and also accepts shorthand like `ipo`, `split`, `earnings`, `earnings_date`. |
| `start_time` | int64 | yes | Start time (Unix timestamp in seconds). For Split/Earnings, max 1 year range. |
| `end_time` | int64 | yes | End time (Unix timestamp in seconds). For Split/Earnings, max 1 year range. |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `type` | string | Event type in snake_case: `ipo_date`, `split_date`, or `earnings_date` |
| `value` | string | The event date (`YYYY-MM-DD` format, e.g. `2026-04-30`) |
