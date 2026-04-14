# Trades

`GET trades`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `user` | string | no | Filter by user wallet address |
| `market` | string | no | Filter by conditionId |
| `asset` | string | no | Filter by CLOB token ID |
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |

**Response** — JSON array of trade objects:

| Field | Type | Description |
|-------|------|-------------|
| `proxyWallet` | string | Trader wallet address |
| `side` | string | Trade side: `"BUY"` or `"SELL"` |
| `asset` | string | CLOB token ID |
| `conditionId` | string | Condition ID (hex) |
| `size` | number | Trade size (shares) |
| `price` | number | Execution price |
| `timestamp` | number | Trade timestamp (Unix seconds) |
| `title` | string | Market title |
| `slug` | string | Market slug |
| `icon` | string | Market icon URL |
| `eventSlug` | string | Parent event slug |
| `outcome` | string | Outcome name |
| `outcomeIndex` | number | Outcome index |
| `name` | string | Trader display name |
| `pseudonym` | string | Trader pseudonym |
| `transactionHash` | string | On-chain transaction hash |
