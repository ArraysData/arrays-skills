# Market trading pairs

`GET /api/v1/market/trading-pairs`

Every `trading_pair` a symbol trades as, grouped by instrument type. Use it to build the `trading_pair` for `market/kline`.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Canonical symbol, 1–10 upper-case letters or digits (`BTC`, `NVDA`, `VOO`, `GCUSD`, `EURUSD`). Dotted non-US symbols are rejected |

Response envelope: `{ "success": true, "request_id": "...", "data": [ ... ] }` — `data` is a one-element array.

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The symbol queried |
| `alias` | string[] | Other names the symbol resolves from (`BTCUSDT`, `Bitcoin`, `$BTC`); often empty |
| `trading_pairs` | object[] | One group per instrument type (below) |

Each entry in `trading_pairs`:

| Field | Type | Description |
|-------|------|-------------|
| `instrument_type` | string | `spot`, `perp`, `option`, `future` |
| `pairs` | object[] | Venues for that instrument type (below) |

Each entry in `pairs`:

| Field | Type | Description |
|-------|------|-------------|
| `trading_pair` | string | Value to pass to `market/kline` (`US_SPOT_NVDA_USD`) |
| `underlying_type` | string | `crypto`, `stock`, `etf`, `commodity`, `fx` |
| `market` | string | `BINANCE`, `HYPERLIQUID`, `US`, `CME`, `FX` |
| `quote` | string | Quote currency (`USDT`, `USDC`, `USD`) |
| `type` | string | Venue product label (`crypto-spot`); often empty |
| `fee_rate` | float64 | Venue taker fee as a decimal; `0` when unknown |
| `description` | string | Often empty |
| `symbol_icon_url` | string | Often empty |
| `alias` | string[] | Often empty |

The same ticker can mean different things on different venues — `SPX` is a memecoin perp on Binance and Hyperliquid, while the S&P 500 index is `US_SPOT_SPX_USD`. Check `underlying_type` before picking a pair.
