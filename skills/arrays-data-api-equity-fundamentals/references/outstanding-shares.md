# Outstanding shares

`GET /api/v1/stocks/outstanding-shares`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol |
| `period_type` | string | yes | `quarterly` or `annual` (default `quarterly`) |
| `start_time` | int64 | yes | Unix seconds |
| `end_time` | int64 | yes | Unix seconds |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `description` | string | Description text |
| `date` | string | Date |
| `period` | string | Period type |
| `fiscal_year` | string | Fiscal year |
| `fiscal_quarter` | string | Fiscal quarter |
| `total_outstanding` | float64 | Total outstanding shares |
| `unit` | string | Unit of measurement |
| `adr_description` | string | ADR description (may be null) |
| `adr_ratio` | float64 | ADR ratio (may be null) |
| `adr_fsym_id` | string | ADR FactSet symbol ID (may be null) |
| `adr_total_outstanding` | float64 | ADR total outstanding (may be null) |
