# Trading pair

`GET /api/v1/crypto/trading-pair`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `base` | string | yes | Base currency (e.g. `BTC`) |
| `quote` | string | yes | Quote currency (e.g. `USDT`) |

**Response fields** — `data` is an array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int32 | Unique trading pair identifier |
| `exchange` | string | Exchange name (e.g. `"binance"`) |
| `base` | string | Base currency (e.g. `"BTC"`) |
| `quote` | string | Quote currency (e.g. `"USDT"`) |
| `instrument_type` | int16 or null | Instrument type identifier |
| `symbol` | string | Trading pair symbol (e.g. `"BTCUSDT"`) |
| `is_valid` | boolean | Whether the pair is currently valid/active |
