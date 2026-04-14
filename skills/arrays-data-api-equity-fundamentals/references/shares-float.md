# Shares float

`GET /api/v1/stocks/shares-float`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol, uppercase |

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | Data date and time |
| `free_float` | float64 | Free float percentage |
| `float_shares` | string | Number of float shares |
| `outstanding_shares` | string | Number of outstanding shares |
| `source` | string | Data source URL (SEC filing link) |
