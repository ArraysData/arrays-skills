# On-chain metrics

`GET /api/v1/crypto/metrics/realized-price`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (**only `BTC` supported currently**) |
| `start_time` | int64 | yes | Unix seconds |
| `end_time` | int64 | yes | Unix seconds |
| `limit` | int32 | no | Max results (1-1000). If not set, returns all matched data |

**Response fields** — V2 wrapper (`data` is an array). Each metric has its own fields:

**`metrics/mvrv`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `mvrv_ratio` | float64 | MVRV ratio value |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time (`YYYY-MM-DD HH:mm:ss`, UTC+0) |

**`metrics/realized-price`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `realized_price` | float64 | Realized price in USD |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time |

**`metrics/nupl`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `nupl` | float64 | Net unrealized profit/loss |
| `nup` | float64 | Net unrealized profit |
| `nul` | float64 | Net unrealized loss |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time |

**`metrics/leverage-ratio`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `leverage_ratio` | float64 | Estimated leverage ratio |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time |

**`metrics/ssr`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `ssr` | float64 | Stablecoin supply ratio |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time |
