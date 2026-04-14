# 2. Economic indicators

`GET /api/v1/macro/economic-indicators`

**Timestamp Rule**: Convert dates in the indicator / event's local timezone to unix time first before querying. E.g., For US data, use US Eastern Time when computing unix timestamps.

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `indicator_type` | string | yes | Indicator type enum (see list below) |
| `time_type` | string | yes | Time filter type: `OBSERVED_AT` (filter by publish timestamp) or `CALENDAR_START_DATE` (filter by calendar date) |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds, must be > start_time) |

**Supported `indicator_type` values** (36 indicators):

- GDP indicators: `GDP`, `REAL_GDP`, `REAL_GDP_PER_CAPITA`
- Employment: `INITIAL_CLAIMS`, `UNEMPLOYMENT_RATE`, `TOTAL_NONFARM_PAYROLL`
- Interest rates: `FEDERAL_FUNDS`
- Inflation / prices: `CPI`, `CORE_CPI`, `INFLATION_RATE_YOY` (published annually), `PPI`
- Consumer: `CONSUMER_SENTIMENT`, `CONSUMER_INFLATION_EXPECTATIONS`, `RETAIL_SALES`
- Production: `DURABLE_GOODS`, `INDUSTRIAL_PRODUCTION`
- Recession: `SMOOTHED_RECESSION_PROBABILITIES`
- TIPS (Treasury Inflation-Indexed): `TIPS_2_YEAR`, `TIPS_5_YEAR`, `TIPS_10_YEAR`, `TIPS_20_YEAR`, `TIPS_30_YEAR`
- Volatility: `VIX`, `GOLD_VIX`, `CRUDE_OIL_VIX`, `RUSSELL_2000_VIX`
- Treasury yields: `TREASURY_YIELD_1_MONTH`, `TREASURY_YIELD_3_MONTH`, `TREASURY_YIELD_6_MONTH`, `TREASURY_YIELD_2_YEAR`, `TREASURY_YIELD_5_YEAR`, `TREASURY_YIELD_10_YEAR`, `TREASURY_YIELD_20_YEAR`, `TREASURY_YIELD_30_YEAR`

**Important tips for `time_type`:**
- Use `CALENDAR_START_DATE` to filter by the period the data refers to (e.g., January 2025 CPI = date `2025-01-01`).
- Use `OBSERVED_AT` to filter by the date the data was published/released.
- **If `CALENDAR_START_DATE` returns empty for a recent period**, try widening the window by +/- 30 days, or switch to `OBSERVED_AT`.
- **To check if a specific indicator was announced on a given date**: Use `time_type=OBSERVED_AT` with `start_time`/`end_time` covering that day. Then check the `date` field in the response to see which period the released data refers to.
- **CRITICAL: Always filter observations by the `date` field.** The `observations` array may contain data for multiple months/quarters. Do NOT blindly use `observations[0]` — instead, match the `date` field to the target period. For example, when querying January 2025 data, filter for `date` starting with `"2025-01"`:
```python
obs = [o for o in indicator["observations"] if o["date"].startswith("2025-01")]
value = obs[0]["value"] if obs else None
```

**Response** — `data` is an array containing one object with `series` and `observations`:
```json
{
  "success": true,
  "request_id": "...",
  "data": [
    {
      "series": { "name": "CPI", "title": "Consumer Price Index", "frequency": "Monthly", "units": "Index 1982-1984=100", ... },
      "observations": [
        { "date": "2024-12-01", "value": 315.605, "release_date": "2025-01-15", "observed_at": 1736899200 }
      ]
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `data[0].series.name` | string | Series ID (e.g. `GDP`) |
| `data[0].series.title` | string | Series title (e.g. `Gross Domestic Product`) |
| `data[0].series.seasonal_adjustment` | string | Seasonal adjustment type |
| `data[0].series.frequency` | string | Data frequency (e.g. `Quarterly`) |
| `data[0].series.units` | string | Data units (e.g. `Billions of Dollars`) |
| `data[0].series.notes` | string | Series notes/description (optional) |
| `data[0].observations[]` | array | Array of observation data points |
| `data[0].observations[].date` | string | Observation date (e.g. `2024-01-15`) |
| `data[0].observations[].value` | float | Indicator value |
| `data[0].observations[].release_date` | string | First release date (e.g. `2024-04-25`) |
| `data[0].observations[].observed_at` | integer | Observation publish timestamp (Unix seconds) |

**Python example:**
```python
import requests, os, calendar
from datetime import datetime, timezone
base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

# ALWAYS compute timestamps with datetime — never hardcode
def to_ts(y, m, d):
    return int(calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple()))

# Get CPI data for December 2024
resp = requests.get(f"{base}/api/v1/macro/economic-indicators",
    params={"indicator_type": "CPI", "time_type": "CALENDAR_START_DATE",
            "start_time": to_ts(2024, 12, 1), "end_time": to_ts(2025, 1, 1)},
    headers={"X-API-Key": key})
body = resp.json()
indicator = body["data"][0]  # first (and only) element in data array
series = indicator["series"]
observations = indicator["observations"]
# IMPORTANT: Always filter by date — observations may contain multiple periods
target_obs = [o for o in observations if o["date"].startswith("2024-12")]
if target_obs:
    print(f"{target_obs[0]['date']}: {target_obs[0]['value']} (units: {series['units']})")
```

---
