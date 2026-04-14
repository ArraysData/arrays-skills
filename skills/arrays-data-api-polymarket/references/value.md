# Value

`GET value`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `user` | string | **yes** | User wallet address (proxy wallet) |

**Response** — JSON array with a single object:

| Field | Type | Description |
|-------|------|-------------|
| `user` | string | User wallet address |
| `value` | number | Total portfolio value in USD |
