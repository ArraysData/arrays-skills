# Fear & greed index

`GET /api/v1/crypto/fear-greed-index`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds) |

**Response fields** — V2 wrapper (`data` is an array of objects):

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | int64 | Unix timestamp in seconds |
| `value` | float64 or null | Fear & greed index value (null when unavailable) |
| `time` | string | Formatted time (`YYYY-MM-DD hh:mm:ss`, UTC+0) |
