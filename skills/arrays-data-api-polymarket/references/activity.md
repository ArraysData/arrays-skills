# Activity

`GET activity`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `user` | string | **yes** | User wallet address (proxy wallet) |
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |

**Response** — JSON array of activity objects:

| Field | Type | Description |
|-------|------|-------------|
| `proxyWallet` | string | User wallet address |
| `timestamp` | number | Activity timestamp (Unix seconds) |
| `conditionId` | string | Condition ID (hex) |
| `type` | string | Activity type (e.g. `"TRADE"`, `"REDEEM"`, `"SPLIT"`, `"MERGE"`) |
| `size` | number | Size in shares |
| `usdcSize` | number | Size in USDC |
| `transactionHash` | string | On-chain transaction hash |
| `price` | number | Price at time of activity |
| `asset` | string | CLOB token ID |
| `side` | string | Trade side (`"BUY"` or `"SELL"`) |
| `outcomeIndex` | number | Outcome index |
| `title` | string | Market title |
| `slug` | string | Market slug |
| `icon` | string | Market icon URL |
| `eventSlug` | string | Parent event slug |
| `outcome` | string | Outcome name |
| `name` | string | User display name |
| `pseudonym` | string | User pseudonym |
