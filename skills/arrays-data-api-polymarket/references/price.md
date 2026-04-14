# Price

`GET price`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token_id` | string | **yes** | CLOB token ID |
| `side` | string | **yes** | `"buy"` or `"sell"` |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `price` | string | Current price (decimal string, e.g. `"0.216"`) |
