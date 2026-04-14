# On-chain metrics with time_type

`GET /api/v1/crypto/metrics/whale-ratio`

Same as above plus:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `time_type` | string | no | `DATE` (default) or `OBSERVED_AT` |

**Response fields** — V2 wrapper (`data` is an array). Each metric has its own fields:

**`metrics/whale-ratio`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `whale_ratio` | float64 | Exchange whale ratio |
| `observed_at` | int64 | Unix timestamp in seconds |
| `date` | string | Date string (`YYYY-MM-DD`) |

**`metrics/inflow-cdd`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `inflow_cdd` | float64 | Exchange inflow coin days destroyed |
| `observed_at` | int64 | Unix timestamp in seconds |
| `date` | string | Date string |

**`metrics/miner-to-exchange`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `flow_amount` | float64 | Total flow amount |
| `flow_mean` | float64 | Mean flow amount |
| `flow_count` | int64 | Number of flow transactions |
| `observed_at` | int64 | Unix timestamp in seconds |
| `date` | string | Date string |

**`metrics/sopr`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `sopr` | float64 | Spent output profit ratio |
| `observed_at` | int64 | Unix timestamp in seconds |
| `date` | string | Date string |

**`metrics/puell-multiple`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `puell_multiple` | float64 | Puell multiple value |
| `observed_at` | int64 | Unix timestamp in seconds |
| `date` | string | Date string |
