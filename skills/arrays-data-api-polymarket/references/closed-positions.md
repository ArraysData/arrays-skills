# Closed positions

`GET closed-positions`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `user` | string | **yes** | User wallet address (proxy wallet) |
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |

**Response** — JSON array of closed position objects:

| Field | Type | Description |
|-------|------|-------------|
| `proxyWallet` | string | User proxy wallet address |
| `asset` | string | CLOB token ID |
| `conditionId` | string | Condition ID (hex) |
| `avgPrice` | number | Average entry price |
| `totalBought` | number | Total shares bought |
| `realizedPnl` | number | Realized P&L in USDC |
| `curPrice` | number | Final price (0 or 1) |
| `title` | string | Market title |
| `slug` | string | Market slug |
| `icon` | string | Market icon URL |
| `eventSlug` | string | Parent event slug |
| `outcome` | string | Outcome name |
| `outcomeIndex` | number | Outcome index |
| `oppositeOutcome` | string | Opposite outcome name |
| `oppositeAsset` | string | Opposite outcome token ID |
| `endDate` | string | Market end date (ISO 8601) |
| `timestamp` | number | Settlement timestamp (Unix seconds) |
