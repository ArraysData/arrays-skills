# Event screener

`GET /api/v1/stocks/screener/events`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `event_type` | string | yes | `IPO Date`, `Split Date`, or `Earnings Date` |
| `start_time` | int64 | yes | Start time (Unix timestamp in seconds). For Split/Earnings, max 1 year range. |
| `end_time` | int64 | yes | End time (Unix timestamp in seconds). For Split/Earnings, max 1 year range. |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `type` | string | Event type matched (e.g. `IPO Date`, `Split Date`, `Earnings Date`) |
| `value` | string | The event date or related value |
