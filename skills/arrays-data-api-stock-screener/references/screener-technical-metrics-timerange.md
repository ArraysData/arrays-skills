# Technical metrics screener — time range

`GET /api/v1/stocks/screener/technical-metrics/timerange`

Same filtering as `screener/technical-metrics` but over a date range. Results are grouped by date (`YYYY-MM-DD`).

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | integer | yes | Start time (Unix seconds, UTC) |
| `end_time` | integer | yes | End time (Unix seconds, UTC) |
| `metric_type` | string | yes | Technical metric (same list as `screener-technical-metrics.md`) |
| `range_min` | float64 | no | Min value filter — returns stocks with value ≥ `range_min` |
| `range_max` | float64 | no | Max value filter — returns stocks with value ≤ `range_max` |
| `order_by` | string | no | Sort by metric value within each day: `ASC` or `DESC` (default `DESC`) |
| `limit` | integer | no | Max results per day (default no limit) |
| `symbol_type` | string | no | Asset type filter: `stock` (CS/ADRC) or `etf`. Default `stock`. |

## Response

```json
{
  "success": true,
  "data": [
    {
      "date": "2026-04-24",
      "items": [
        {
          "symbol": "TFII",
          "snapshot_time": 1777060800,
          "metric": "rsi_14",
          "value": 79.614817
        }
      ]
    }
  ],
  "request_id": "..."
}
```

**Each item in `data` (date bucket):**

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date for this bucket (`YYYY-MM-DD`) |
| `items` | array | Stocks matching the filter on this date |

**Each object in `items`:**

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `snapshot_time` | int64 | Snapshot time for this row (Unix seconds, UTC) |
| `metric` | string | Metric type identifier — note: returned in lowercase by this endpoint (e.g. `rsi_14`) |
| `value` | float64 | Metric value for this stock on this date |
