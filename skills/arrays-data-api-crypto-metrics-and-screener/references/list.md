# Token list by chain

`GET /api/v1/crypto/list`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `chain_type` | int | yes | 0=BTC, 1=ETH, 2=BSC, 3=BASE, 4=SOL, 99=OTHER |
| `symbol` | string | no | Filter by symbol (case-insensitive partial match) |
| `limit` | int | yes | Items per page (default 10, max 500) |
| `offset` | int | no | Pagination offset (default 0) |

**Response fields** — `data` is an array of token objects:

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `trade_pair_id` | int32 | Trading pair identifier |
| `address` | string | Token contract address |
| `chain_type` | int16 | Blockchain type identifier |
| `symbol` | string | Token symbol (e.g. `"BTC"`) |
| `logo` | string | Token logo URL |
| `twitter_url` | string | Twitter profile URL |
| `website_url` | string | Website URL |
| `price_change` | string | Price change ratio (as string, e.g. `"0.033"`) |
| `open_price` | string | Open price (as string) |
| `close_price` | string | Close price (as string) |
| `high_price` | string | High price (as string) |
| `low_price` | string | Low price (as string) |
| `total_volume` | string | Total trading volume (as string) |
