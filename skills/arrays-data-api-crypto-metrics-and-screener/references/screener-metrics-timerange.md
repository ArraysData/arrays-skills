# Crypto metrics screener time range

`GET /api/v1/crypto/screener/metrics/timerange`

Same as snapshot variant, but replace `snapshot` with `start_time`, `end_time`, and optional `limit`.

**Response fields** — V2 wrapper (`data` is an array of date-grouped objects):

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date string (`YYYY-MM-DD`) |
| `items` | array | Array of metric data points for this date |

Each item in `items`:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `snapshot_time` | int64 | Snapshot time in Unix seconds |
| `metric` | string | Metric type identifier |
| `value` | float64 | Metric value |
