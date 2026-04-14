# Order book

`GET book`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token_id` | string | **yes** | CLOB token ID |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `market` | string | Condition ID (hex) |
| `asset_id` | string | CLOB token ID |
| `timestamp` | string | Timestamp in milliseconds (string) |
| `hash` | string | Order book state hash |
| `bids` | array | Array of bid orders |
| `asks` | array | Array of ask orders |

Each bid/ask order:

| Field | Type | Description |
|-------|------|-------------|
| `price` | string | Price level (decimal string) |
| `size` | string | Size at this price level (decimal string) |

Bids are sorted by price descending (best bid first). Asks are sorted by price ascending (best ask first).

Additional top-level response fields:

| Field | Type | Description |
|-------|------|-------------|
| `min_order_size` | string | Minimum order size (e.g. `"1"`) |
| `tick_size` | string | Minimum price increment (e.g. `"0.01"`) |
| `neg_risk` | bool | Whether the market uses neg-risk framework |
| `last_trade_price` | string | Last trade price (decimal string, e.g. `"0.45"`) |
