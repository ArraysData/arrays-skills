# Fiscal dates by range

`GET /api/v1/stocks/fiscal-dates/range`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol |
| `start_time` | int64 | yes | Start time (Unix seconds), matches by `calendar_end` (NOT `public_date`) |
| `end_time` | int64 | yes | End time (Unix seconds), matches by `calendar_end` (NOT `public_date`) |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `fiscal_year` | int32 | Fiscal year |
| `fiscal_quarter` | string | Fiscal quarter (`Q1`-`Q4`, `FY`) |
| `calendar_end` | string | End date of the fiscal period (`YYYY-MM-DD`) |
| `public_date` | string | Date earnings report was publicly released (`YYYY-MM-DD`), empty if not available |
