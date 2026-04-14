# Token detail

`GET crypto/detail`

Response envelope: `{ "request_id": "...", "data": [ ... ] }` — `data` is always an array of Token objects.

**Each item in `data` (Token):**

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Trade pair ID | `trade_pair_id` | integer | Internal trading pair identifier |
| Address | `address` | string | Token contract address |
| Chain type | `chain_type` | integer | Blockchain type identifier (e.g. 1 = ETH) |
| Symbol | `symbol` | string | Token symbol (e.g. `"BTC"`) |
| Logo | `logo` | string | URL to the token logo image |
| Twitter URL | `twitter_url` | string | Token Twitter/X profile URL |
| Website URL | `website_url` | string | Token official website URL |
| Price change | `price_change` | string | Price change ratio over the interval (e.g. `"0.033"` = 3.3%) |
| Open price | `open_price` | string | Opening price (string for precision) |
| Close price | `close_price` | string | Closing / current price (string for precision) |
| High price | `high_price` | string | Highest price in the interval (string for precision) |
| Low price | `low_price` | string | Lowest price in the interval (string for precision) |
| Total volume | `total_volume` | string | Total trading volume (string for precision) |
