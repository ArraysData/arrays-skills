# Holders

`GET holders`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `market` | string | **yes** | Condition ID (hex) |
| `limit` | int | no | Number of top holders per token |

**Response** — JSON array of token-grouped holder objects:

| Field | Type | Description |
|-------|------|-------------|
| `token` | string | CLOB token ID |
| `holders` | array | Array of holder objects |

Each holder object:

| Field | Type | Description |
|-------|------|-------------|
| `proxyWallet` | string | Holder wallet address |
| `asset` | string | CLOB token ID |
| `amount` | number | Number of shares held |
| `outcomeIndex` | number | Outcome index |
| `name` | string | Display name |
| `pseudonym` | string | Pseudonym |
| `verified` | bool | Whether account is verified |
