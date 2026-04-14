# Positions

`GET positions`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `user` | string | **yes** | User wallet address (proxy wallet) |
| `market` | string | no | Filter by conditionId |
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |

**Response** — JSON array of position objects:

| Field | Type | Description |
|-------|------|-------------|
| `proxyWallet` | string | User proxy wallet address |
| `asset` | string | CLOB token ID |
| `conditionId` | string | Condition ID (hex) |
| `size` | number | Position size (shares) |
| `avgPrice` | number | Average entry price |
| `initialValue` | number | Initial USDC value |
| `currentValue` | number | Current value |
| `cashPnl` | number | Cash profit/loss |
| `percentPnl` | number | Percentage P&L |
| `totalBought` | number | Total shares bought |
| `realizedPnl` | number | Realized P&L |
| `percentRealizedPnl` | number | Percentage realized P&L |
| `curPrice` | number | Current market price |
| `redeemable` | bool | Whether position is redeemable |
| `mergeable` | bool | Whether position is mergeable |
| `title` | string | Market title |
| `slug` | string | Market slug |
| `icon` | string | Market icon URL |
| `eventId` | string | Parent event ID |
| `eventSlug` | string | Parent event slug |
| `outcome` | string | Outcome name (e.g. `"Yes"`, `"Up"`) |
| `outcomeIndex` | number | Outcome index (0 or 1) |
| `oppositeOutcome` | string | Opposite outcome name |
| `oppositeAsset` | string | Opposite outcome token ID |
| `endDate` | string | Market end date |
| `negativeRisk` | bool | Whether neg-risk market |
