# Short Interest

`GET /api/v1/stocks/short-interest`

Twice-monthly consolidated short interest for a US equity, reported by
settlement date (mid-month and month-end). Lags settlement by ~8 trading days
(not real time).

#### Request parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (uppercase, e.g., NVDA, BRK.B) |
| `start_time` | integer | No | Range start, Unix seconds (filters the date selected by `time_type`) |
| `end_time` | integer | No | Range end, Unix seconds (filters the date selected by `time_type`) |
| `time_type` | string | No | Which date the range filters: `SETTLEMENT_DATE` (default) or `UPDATED_AT` |

`start_time` and `end_time` are optional but must be sent together (sending only
one returns `VALIDATION_ERROR`); omit both to get the latest period.

#### Response

```json
{
  "success": true,
  "data": [
    {
      "symbol": "NVDA",
      "company_name": "NVIDIA Corporation Common Stoc",
      "settlement_date": "2026-06-30",
      "short_interest": 310126785,
      "last_short_interest": 299666309,
      "change_in_short_interest": 10460476,
      "change_in_short_interest_percentage": 3.49,
      "average_daily_volume": 155989510,
      "days_to_cover": 1.99,
      "short_interest_pct_float": 1.34,
      "short_interest_pct_outstanding": 1.28,
      "updated_at": 1783936830
    }
  ],
  "metadata": { "data_as_of": 1788861634 }
}
```

`metadata.data_as_of` is the unix-seconds freshness stamp of the underlying dataset.

Each element in `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `company_name` | string | Company name |
| `settlement_date` | string | Settlement date of the reporting period |
| `short_interest` | int64 | Shares sold short |
| `last_short_interest` | int64 | Shares sold short in the prior period |
| `change_in_short_interest` | int64 | Change in shares short vs prior period |
| `change_in_short_interest_percentage` | float64 | Change in shares short vs prior period, percent |
| `average_daily_volume` | int64 | Average daily trading volume |
| `days_to_cover` | float64 | Short interest divided by average daily volume |
| `short_interest_pct_float` | float64 | Short interest as percent of float; only set for the latest settlement date |
| `short_interest_pct_outstanding` | float64 | Short interest as percent of shares outstanding; only set for the latest settlement date |
| `updated_at` | int64 | Ingestion time (Unix seconds) |

---
