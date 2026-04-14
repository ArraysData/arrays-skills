# Spread

`GET spread`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token_id` | string | **yes** | CLOB token ID |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `spread` | string | Bid-ask spread (decimal string, e.g. `"0.004"`) |
