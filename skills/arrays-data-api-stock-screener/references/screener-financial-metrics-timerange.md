# Time range variants

`GET /api/v1/stocks/screener/financial-metrics/timerange`

Same as snapshot variants but replace `snapshot` with:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | int | yes | Start (Unix seconds) |
| `end_time` | int | yes | End (Unix seconds) |
| `limit` | int | no | Max results per day |

**Response fields** (each item in `data` array is a date group):

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date in `YYYY-MM-DD` format |
| `items` | array | Array of stock metric data for this date |

Each object in the `items` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `snapshot_time` | integer | Snapshot time as Unix timestamp in seconds (UTC) |
| `metric` | string | Metric type that was queried (e.g. `PE_RATIO`, `MA_5`) |
| `value` | number | Metric value for this stock |
