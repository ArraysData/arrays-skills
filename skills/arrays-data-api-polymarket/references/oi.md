# Open interest

`GET oi`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `market` | string | no | Condition ID to filter; omit for global OI |

**Response** — JSON array of OI objects:

| Field | Type | Description |
|-------|------|-------------|
| `market` | string | Market identifier or `"GLOBAL"` |
| `value` | number | Open interest in USD |
