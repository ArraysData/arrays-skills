# Price history

`GET prices-history`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `market` | string | **yes** | CLOB **token ID** (not condition_id) |
| `interval` | string | no | Time range: `1h`, `6h`, `1d`, `1w`, `1m`, `max`, `all`. The API error message only lists the first five, but `max` and `all` also work (both return full history). Values like `3m`, `6m`, `1y` return 400 errors. |
| `startTs` | number | no | Unix timestamp (seconds) — start of time range. Can be used instead of or with `interval`. |
| `endTs` | number | no | Unix timestamp (seconds) — end of time range. Can be used instead of or with `interval`. |
| `fidelity` | int | no | Sampling interval in minutes (e.g. `fidelity=5` means one data point every 5 minutes, `fidelity=60` means one per hour). Omit for full-resolution data. Avoid very small values as the API may return an empty `history` array silently. |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `history` | array | Array of price data points |

Each data point:

| Field | Type | Description |
|-------|------|-------------|
| `t` | number | Unix timestamp (seconds) |
| `p` | number | Price at that time |

**Rate-limit note**: Rapid consecutive `/prices-history` requests may return HTTP 200 with an empty `history` array (silent failure, no error code). Space requests at least 1 second apart to avoid this.
