# Exchange flows

`GET /api/v1/crypto/exchange-flows`

Get crypto exchange inflow/outflow data for BTC and ETH from Binance. Symbol parameter is case-insensitive.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (case-insensitive, e.g., BTC, btc, ETH, eth) |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `limit` | integer | no | Maximum number of records (default: 50, max: 1000) |
| `window` | string | no | Time window granularity: `hour` or `day`. Default: `hour` |
