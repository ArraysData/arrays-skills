# Fiscal dates

`GET /api/v1/stocks/fiscal-dates`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol |
| `fiscal_year` | int | yes | Fiscal year (e.g. `2024`) |
| `fiscal_quarter` | string | yes | `Q1`, `Q2`, `Q3`, `Q4`, or `FY` |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `fiscal_year` | int32 | Fiscal year |
| `fiscal_quarter` | string | Fiscal quarter (`Q1`-`Q4`, `FY`) |
| `calendar_end` | string | End date of the fiscal period (`YYYY-MM-DD`) |
| `public_date` | string | Date earnings report was publicly released (`YYYY-MM-DD`), empty if not available |
