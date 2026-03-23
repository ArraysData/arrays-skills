---
name: arrays-data-api-crypto-metrics-and-screener
description: Calls Arrays REST APIs for crypto on-chain analytics and screening — fear & greed index, on-chain metrics (MVRV, NUPL, SOPR, realized price, leverage ratio, SSR, whale ratio, Puell multiple, miner-to-exchange, inflow CDD), crypto metrics screener, token lists, trading pairs, DeFi pools (TVL, APY, volume, fees for protocols like Uniswap, Lido, PancakeSwap, etc.), Meteora liquidity, token unlock schedules (cliff and linear allocations for DeFi protocols like Hyperliquid, Arbitrum, Uniswap, etc.), and Bitcoin correlation indices. Use when the user asks about crypto market sentiment, on-chain analysis, token screening, DeFi yields, DeFi pool metrics (TVL, volume, fees), token discovery, protocol token unlock events and vesting schedules, or Bitcoin correlation with other assets.
---

# Arrays Data API — Crypto Metrics and Screener

On-chain analytics (MVRV, NUPL, SOPR, etc.), fear & greed, crypto screener, token lists, trading pairs, DeFi pools.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY`.

## Endpoints

All under prefix `/api/v1/tokens/`:

| Method | Path | Description |
|--------|------|-------------|
| GET | `fear-greed-index` | Crypto fear & greed index |
| GET | `unlock-events` | Token unlock events |
| GET | `market-metrics` | Crypto market metrics |
| GET | `screener/metrics` | Crypto metrics screener (snapshot) |
| GET | `screener/metrics/timerange` | Crypto metrics screener (time range) |
| GET | `metrics/mvrv` | MVRV ratio |
| GET | `metrics/realized-price` | Realized price |
| GET | `metrics/nupl` | Net unrealized profit/loss |
| GET | `metrics/leverage-ratio` | Leverage ratio |
| GET | `metrics/ssr` | Stablecoin supply ratio |
| GET | `metrics/whale-ratio` | Whale ratio |
| GET | `metrics/inflow-cdd` | Inflow coin days destroyed |
| GET | `metrics/miner-to-exchange` | Miner to exchange flow |
| GET | `metrics/sopr` | Spent output profit ratio |
| GET | `metrics/puell-multiple` | Puell multiple |
| GET | `trading_pair` | Trading pair info |
| GET | `list_by_chain` | Token list by blockchain |
| GET | `list_by_filter_cursor` | Token list with filters + cursor pagination |
| **POST** | `defi_pools/list` | DeFi pools list |
| GET | `defi_pools/protocols` | Supported DeFi protocols (no params) |
| GET | `meteora/liquidity_changes` | Meteora liquidity changes |

## Parameters and response fields by endpoint

### Fear & greed index (`fear-greed-index`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds) |

**Response fields** — V2 wrapper (`data` is an array of objects):

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | int64 | Unix timestamp in seconds |
| `value` | float64 or null | Fear & greed index value (null when unavailable) |
| `time` | string | Formatted time (`YYYY-MM-DD hh:mm:ss`, UTC+0) |

### Unlock events (`unlock-events`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token_id` | string | yes | Token identifier (e.g. `arbitrum`, `optimism`, `sui`) |
| `start` | string | no | Start date (`YYYY-MM-DD`) |
| `end` | string | no | End date (`YYYY-MM-DD`) |

**Response fields** — the top-level response body contains:

| Field | Type | Description |
|-------|------|-------------|
| `metadata` | object | Query metadata |
| `metadata.queryDate` | string | ISO 8601 date of the query |
| `status` | boolean | API status |
| `data` | array | Array of unlock event objects |

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `unlockDate` | string | ISO 8601 date of the unlock event |
| `tokenName` | string | Full token name (e.g. `"Arbitrum"`) |
| `tokenSymbol` | string | Token symbol (e.g. `"ARB"`) |
| `listedMethod` | string | Listing method (e.g. `"INTERNAL"`) |
| `dataSource` | string | Data source (e.g. `"Whitepaper"`) |
| `linearUnlocks` | object or null | Linear unlock data (null if not applicable) |
| `cliffUnlocks` | object or null | Cliff unlock data (null if not applicable) |
| `latestUpdateDate` | string | When the data was last updated |

`cliffUnlocks` object:

| Field | Type | Description |
|-------|------|-------------|
| `cliffAmount` | float64 | Total cliff token amount |
| `cliffValue` | float64 | Total cliff value in USD |
| `valueToMarketCap` | float64 | Percentage of market cap |
| `allocationBreakdown` | array | Breakdown by allocation |

`linearUnlocks` object:

| Field | Type | Description |
|-------|------|-------------|
| `linearAmount` | float64 | Total linear token amount |
| `linearValue` | float64 | Total linear value in USD |
| `valueToMarketCap` | float64 | Percentage of market cap |
| `allocationBreakdown` | array | Breakdown by allocation |

Each item in `allocationBreakdown`:

| Field | Type | Description |
|-------|------|-------------|
| `unlockDate` | string | ISO 8601 date |
| `allocationName` | string | Name of allocation (e.g. `"Investors"`) |
| `standardAllocationName` | string | Standardized name (e.g. `"Private Investors"`) |
| `cliffAmount` | float64 | Token amount in this allocation |
| `cliffValue` | float64 | Value in USD |
| `referencePrice` | float64 | Reference price used for calculation |
| `referencePriceUpdatedTime` | string | When reference price was updated |
| `unlockPrecision` | string | Precision of unlock (e.g. `"MONTH"`, `"DAY"`) |

### Market metrics (`market-metrics`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interval` | string | yes | Time interval: `1d`, `1w`, `1m` |
| `indicator` | string | yes | Indicator type (e.g. `MA_20`, `PRICE_CHANGE_1d`, `MARKET_CAP`, `FDV`) |
| `symbol` | string | no | Token symbol (e.g. `BTCUSDT`); returns all if omitted |
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds) |

**Response fields** — V2 wrapper (`data` is an array of per-symbol objects):

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol (e.g. `"BTCUSDT"`) |
| `type` | string | Indicator type (e.g. `"MA_20"`) |
| `values` | array | Array of time-series data points |

Each item in `values`:

| Field | Type | Description |
|-------|------|-------------|
| `observedAt` | int64 | Unix timestamp in seconds |
| `date` | string | Formatted date (`YYYY-MM-DD HH:mm:ss`, UTC+0) |
| `value` | float64 or null | Metric value (null if not available) |
| `metricComponent` | string | Sub-component label (e.g. `"UPPER"`, `"MID"`, `"LOWER"` for Bollinger; `"DIF"`, `"DEA"`, `"HIST"` for MACD). Omitted for single-value indicators |

### On-chain metrics (`metrics/mvrv`, `metrics/realized-price`, `metrics/nupl`, `metrics/leverage-ratio`, `metrics/ssr`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (**only `BTC` supported currently**) |
| `start_time` | int64 | yes | Unix seconds |
| `end_time` | int64 | yes | Unix seconds |
| `limit` | int32 | no | Max results (1-1000). If not set, returns all matched data |

**Response fields** — V2 wrapper (`data` is an array). Each metric has its own fields:

**`metrics/mvrv`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `mvrvRatio` | float64 | MVRV ratio value |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time (`YYYY-MM-DD HH:mm:ss`, UTC+0) |

**`metrics/realized-price`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `realizedPrice` | float64 | Realized price in USD |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time |

**`metrics/nupl`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `nupl` | float64 | Net unrealized profit/loss |
| `nup` | float64 | Net unrealized profit |
| `nul` | float64 | Net unrealized loss |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time |

**`metrics/leverage-ratio`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `leverageRatio` | float64 | Estimated leverage ratio |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time |

**`metrics/ssr`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `ssr` | float64 | Stablecoin supply ratio |
| `timestamp` | int64 | Unix timestamp in seconds |
| `time` | string | Formatted time |

### On-chain metrics with time_type (`metrics/whale-ratio`, `metrics/inflow-cdd`, `metrics/miner-to-exchange`, `metrics/sopr`, `metrics/puell-multiple`)

Same as above plus:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `time_type` | string | no | `date` (default) or `observedAt` |

**Response fields** — V2 wrapper (`data` is an array). Each metric has its own fields:

**`metrics/whale-ratio`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `whaleRatio` | float64 | Exchange whale ratio |
| `observedAt` | int64 | Unix timestamp in seconds |
| `date` | string | Date string (`YYYY-MM-DD`) |

**`metrics/inflow-cdd`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `inflowCdd` | float64 | Exchange inflow coin days destroyed |
| `observedAt` | int64 | Unix timestamp in seconds |
| `date` | string | Date string |

**`metrics/miner-to-exchange`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `flowAmount` | float64 | Total flow amount |
| `flowMean` | float64 | Mean flow amount |
| `flowCount` | int64 | Number of flow transactions |
| `observedAt` | int64 | Unix timestamp in seconds |
| `date` | string | Date string |

**`metrics/sopr`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `sopr` | float64 | Spent output profit ratio |
| `observedAt` | int64 | Unix timestamp in seconds |
| `date` | string | Date string |

**`metrics/puell-multiple`** — each item:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `puellMultiple` | float64 | Puell multiple value |
| `observedAt` | int64 | Unix timestamp in seconds |
| `date` | string | Date string |

### Trading pair (`trading_pair`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `base` | string | yes | Base currency (e.g. `BTC`) |
| `quote` | string | yes | Quote currency (e.g. `USDT`) |

**Response fields** — Standard wrapper (`response` is a single object):

| Field | Type | Description |
|-------|------|-------------|
| `id` | int32 | Unique trading pair identifier |
| `exchange` | string | Exchange name (e.g. `"binance"`) |
| `base` | string | Base currency (e.g. `"BTC"`) |
| `quote` | string | Quote currency (e.g. `"USDT"`) |
| `instrumentType` | int16 or null | Instrument type identifier |
| `symbol` | string | Trading pair symbol (e.g. `"BTCUSDT"`) |
| `isValid` | boolean | Whether the pair is currently valid/active |

### Token list by chain (`list_by_chain`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `chain_type` | int | yes | 0=BTC, 1=ETH, 2=BSC, 3=BASE, 4=SOL, 99=OTHER |
| `symbol` | string | no | Filter by symbol (case-insensitive partial match) |
| `limit` | int | yes | Items per page (default 10, max 500) |
| `offset` | int | no | Pagination offset (default 0) |

**Response fields** — Standard wrapper (`response` is an array of token objects, with `total` count):

Each item in `response`:

| Field | Type | Description |
|-------|------|-------------|
| `tradePairId` | int32 | Trading pair identifier |
| `address` | string | Token contract address |
| `chainType` | int16 | Blockchain type identifier |
| `symbol` | string | Token symbol (e.g. `"BTC"`) |
| `logo` | string | Token logo URL |
| `twitterUrl` | string | Twitter profile URL |
| `websiteUrl` | string | Website URL |
| `priceChange` | string | Price change ratio (as string, e.g. `"0.033"`) |
| `openPrice` | string | Open price (as string) |
| `closePrice` | string | Close price (as string) |
| `highPrice` | string | High price (as string) |
| `lowPrice` | string | Low price (as string) |
| `totalVolume` | string | Total trading volume (as string) |

### Token list with filters (`list_by_filter_cursor`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | yes | Items per page (default 10, max 500) |
| `cursor` | string | no | Pagination cursor (empty for first page) |
| `interval` | string | no | Time window: `1min`, `15min`, `60min`, `24h`. Required if start/end_time not provided |
| `start_time` | int | no | Unix seconds (alternative to interval) |
| `end_time` | int | no | Unix seconds (alternative to interval) |
| `min_price` / `max_price` | number | no | Price range filter |
| `min_volume` / `max_volume` | number | no | Volume range filter |
| `min_price_change` / `max_price_change` | number | no | Price change range filter |
| `chain_type` | int | no | 0=BTC, 1=ETH, 2=BSC, 3=BASE, 4=SOL, 99=OTHER |
| `symbol` | string | no | Filter by symbol (case-insensitive) |
| `sort_by` | string | no | `price`, `volume`, `price_change` (default `volume`) |
| `sort_direction` | string | no | `ASC` or `DESC` (default `DESC`) |

**Response fields** — Standard wrapper (`response` is an array of token objects, with `pagination`):

Each item in `response` has the same fields as `list_by_chain` (see above):

| Field | Type | Description |
|-------|------|-------------|
| `tradePairId` | int32 | Trading pair identifier |
| `address` | string | Token contract address |
| `chainType` | int16 | Blockchain type identifier |
| `symbol` | string | Token symbol |
| `logo` | string | Token logo URL |
| `twitterUrl` | string | Twitter profile URL |
| `websiteUrl` | string | Website URL |
| `priceChange` | string | Price change ratio (as string) |
| `openPrice` | string | Open price (as string) |
| `closePrice` | string | Close price (as string) |
| `highPrice` | string | High price (as string) |
| `lowPrice` | string | Low price (as string) |
| `totalVolume` | string | Total trading volume (as string) |

Top-level pagination fields:

| Field | Type | Description |
|-------|------|-------------|
| `pagination.next_cursor` | string or null | Cursor for the next page (null if no more) |
| `pagination.has_more` | boolean | Whether more pages exist |

### Crypto metrics screener (`screener/metrics`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `snapshot` | int | yes | Snapshot time (Unix seconds) |
| `metric_type` | string | yes | See metric types below |
| `range_min` | float64 | no | Min value filter |
| `range_max` | float64 | no | Max value filter |
| `order_by` | string | no | `ASC` or `DESC` (default `DESC`) |

**Crypto metric types**: `MARKET_CAP`, `FDV`, `SHARES_VOLUME`, `PRICE_CHANGE_1D/1W/1M/3M/6M/YTD/1Y/3Y/5Y`, `MA_5/10/20/60/120/200`, `EMA_5/10/20/60/120/200`, `RSI_14`, `MACD_DIF/DEA/HIST`, `BOLLINGER_UPPER/MID/LOWER`, `BETA`, `VOLATILITY_20/60/90`

**Response fields** — V2 wrapper (`data` is an array):

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol (e.g. `"BTC"`) |
| `snapshotTime` | int64 | Snapshot time in Unix seconds |
| `date` | string | Date string (`YYYY-MM-DD`) |
| `metric` | string | Metric type identifier (e.g. `"MARKET_CAP"`) |
| `value` | float64 | Metric value |

### Crypto metrics screener time range (`screener/metrics/timerange`)

Same as snapshot variant, but replace `snapshot` with `start_time`, `end_time`, and optional `limit`.

**Response fields** — V2 wrapper (`data` is an array of date-grouped objects):

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date string (`YYYY-MM-DD`) |
| `items` | array | Array of metric data points for this date |

Each item in `items`:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Token symbol |
| `snapshotTime` | int64 | Snapshot time in Unix seconds |
| `metric` | string | Metric type identifier |
| `value` | float64 | Metric value |

### DeFi pools (`defi_pools/list` — POST)

**Body** (JSON):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `from_ts` | string | no | Start time (RFC3339, e.g. `2025-07-01T23:59:59Z`) |
| `to_ts` | string | no | End time (RFC3339) |
| `protocols` | string[] | no | Protocol names (e.g. `["uniswap-v3", "lido"]`) |
| `min_avg_apy` | float64 | no | Min average APY |
| `min_avg_tvl` | float64 | no | Min average TVL |

These fields can also be passed as query parameters.

**Response fields** — V2 wrapper (`data` is a single object):

Top-level `data` object:

| Field | Type | Description |
|-------|------|-------------|
| `count` | int | Number of matching pools |
| `filters` | object | Echo of the applied filters |
| `results` | array | Array of pool objects |

`filters` object:

| Field | Type | Description |
|-------|------|-------------|
| `from_ts` | string | Applied start time |
| `to_ts` | string | Applied end time |
| `protocols` | string[] | Applied protocol filter |
| `min_avg_apy` | float64 | Applied minimum APY |
| `min_avg_tvl` | float64 | Applied minimum TVL |

Each item in `results`:

| Field | Type | Description |
|-------|------|-------------|
| `pool_id` | string | Unique pool identifier (e.g. `"uniswap-v4-0x21c6..."`) |
| `pool_name` | string | Pool display name (e.g. `"ETH/USDC"`) |
| `pool_url` | string | URL to the pool page (may be empty) |
| `chain_name` | string | Blockchain name (e.g. `"ethereum"`, `"unichain"`) |
| `protocol` | string | Protocol name (e.g. `"uniswap-v4"`) |
| `fee_tier` | string | Fee tier (e.g. `"0.05%"`) |
| `lp_type` | string | LP type (may be empty) |
| `maturity_time` | string | Maturity time for time-locked pools (may be empty) |
| `avg_apy` | float64 | Average APY (percentage, e.g. `43.21` means 43.21%) |
| `avg_tvl` | float64 | Average TVL in USD |

### DeFi protocols (`defi_pools/protocols`)

No request parameters.

**Response fields** — V2 wrapper (`data` is a single object):

Top-level `data` object:

| Field | Type | Description |
|-------|------|-------------|
| `count` | int | Total number of supported protocols |
| `results` | array | Array of protocol objects |

Each item in `results`:

| Field | Type | Description |
|-------|------|-------------|
| `protocol` | string | Protocol identifier (e.g. `"uniswap-v3"`, `"lido"`) |

### Meteora liquidity changes (`meteora/liquidity_changes`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `interval` | string | yes | Time interval: `5min`, `15min`, `1h` |
| `min_liquidity_change` | int64 | no | Minimum liquidity change threshold |
| `order_desc` | boolean | no | Sort descending if `true` |
| `limit` | int32 | no | Max results (1-100, default 10) |
| `filter_type` | string | no | `all` (default), `add_only`, `remove_only`, `net_positive`, `net_negative` |

**Response fields** — V2 wrapper (`data` is a single object):

Top-level `data` object:

| Field | Type | Description |
|-------|------|-------------|
| `data` | array | Array of liquidity change records |
| `count` | int | Number of records returned |
| `interval` | string | Applied time interval |
| `filters` | object | Applied filter settings |

`filters` object:

| Field | Type | Description |
|-------|------|-------------|
| `interval` | string | Time interval |
| `min_liquidity_change` | int64 or null | Applied minimum threshold |
| `filter_type` | string | Applied filter type |
| `order_desc` | boolean | Applied sort order |
| `limit` | int32 | Applied result limit |

Each item in `data.data`:

| Field | Type | Description |
|-------|------|-------------|
| `pool_id` | string | Pool identifier |
| `pool_name` | string | Pool display name (may be empty) |
| `token_pair` | string | Token pair (e.g. `"SOL/USDC"`) |
| `timestamp` | int64 | Unix timestamp in seconds |
| `liquidity_change` | int64 | Liquidity change amount in USD equivalent |
| `change_type` | string | Change type: `"add"` or `"remove"` |
| `percentage_change` | float64 | Change as percentage |
| `volume_impact` | int64 or null | Impact on trading volume (may be null) |
| `transaction_hash` | string | Transaction hash (may be empty) |
| `user_address` | string | User wallet address (may be empty) |
| `token0_symbol` | string | First token symbol |
| `token1_symbol` | string | Second token symbol |
| `token0_amount` | string or null | First token amount (may be null) |
| `token1_amount` | string or null | Second token amount (may be null) |
| `price_impact` | float64 or null | Price impact (may be null) |

## Response format

**Standard** (token lists, trading pair):
```json
{ "success": true, "response": [...], "total": 42, "pagination": { "next_cursor": "...", "has_more": true }, "request_id": "..." }
```

**V2** (on-chain metrics, screener, DeFi pools):
```json
{ "success": true, "data": [...], "request_id": "..." }
```

**Error**:
```json
{ "success": false, "error": { "code": "...", "message": "..." }, "request_id": "..." }
```

## Pagination

- `list_by_filter_cursor`: Cursor-based. Pass `cursor` from `pagination.next_cursor`. Loop until `has_more` is false.
- `list_by_chain`: Offset-based. Use `offset` + `limit`.

## Python examples

```python
import requests, os, calendar
from datetime import datetime, timezone

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]
headers = {"X-API-Key": key}

def to_ts(year, month, day):
    return int(calendar.timegm(datetime(year, month, day, tzinfo=timezone.utc).timetuple()))

# On-chain metric: MVRV for BTC
resp = requests.get(f"{base}/api/v1/tokens/metrics/mvrv",
    params={"symbol": "BTC", "start_time": to_ts(2025, 1, 1), "end_time": to_ts(2025, 7, 1), "limit": 30},
    headers=headers)
body = resp.json()
if body["success"]:
    for item in body["data"]:  # V2 format: flat data array
        print(f"MVRV: {item['mvrvRatio']}")

# Token unlock events for Arbitrum
resp = requests.get(f"{base}/api/v1/tokens/unlock-events",
    params={"token_id": "arbitrum", "start": "2025-01-01", "end": "2025-12-31"},
    headers=headers)
body = resp.json()
for event in body.get("data", []):
    if event.get("cliffUnlocks"):
        print(f"Cliff unlock: {event['cliffUnlocks']['cliffAmount']} tokens")
    if event.get("linearUnlocks"):
        print(f"Linear unlock: {event['linearUnlocks']['linearAmount']} tokens")
```

## Bitcoin Correlation with Other Assets

To compute the correlation between Bitcoin and another asset (e.g., TLT, SPY, gold), fetch kline data for both assets, align on common dates, and compute **Pearson correlation of price levels** (NOT returns).

**Steps**:
1. Fetch BTC daily kline from `/api/v1/tokens/kline` (use `symbol=BTC`)
2. Fetch the other asset's daily kline from `/api/v1/stocks/kline` (for stocks/ETFs like TLT, use `ticker=TLT`)
3. Build date→close_price maps for both
4. Find common dates (dates where both have data). TLT only trades on business days — use only dates present in BOTH datasets
5. Compute **Pearson correlation of the closing price series** (price levels, NOT returns)

**CRITICAL**: Use **price levels** for correlation, NOT daily returns. This is the standard methodology for the Bitcoin correlation index.

```python
import requests, os, calendar, math
from datetime import datetime, timezone

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]

def to_ts(y, m, d):
    return int(calendar.timegm(datetime(y, m, d, tzinfo=timezone.utc).timetuple()))

# 30-day window ending Sep 28, 2025
start = to_ts(2025, 8, 28)
end = to_ts(2025, 9, 29)

# Fetch BTC kline
resp1 = requests.get(f"{base}/api/v1/tokens/kline",
    params={"symbol": "BTC", "start_time": start, "end_time": end, "interval": "1d", "limit": 40},
    headers={"X-API-Key": key})
btc_data = resp1.json()["response"]["data"]

# Fetch TLT kline (ETF — use stocks endpoint)
resp2 = requests.get(f"{base}/api/v1/stocks/kline",
    params={"ticker": "TLT", "start_time": start, "end_time": end, "interval": "1d", "limit": 40},
    headers={"X-API-Key": key})
tlt_data = resp2.json()["response"]["data"]

# Build date -> close maps
btc_prices = {c["time_period_start"][:10]: c["price_close"] for c in btc_data}
tlt_prices = {c["time_period_start"][:10]: c["price_close"] for c in tlt_data}

# Common dates only (align on trading days)
common = sorted(set(btc_prices) & set(tlt_prices))
btc_vals = [btc_prices[d] for d in common]
tlt_vals = [tlt_prices[d] for d in common]

# Pearson correlation of PRICE LEVELS
n = len(btc_vals)
mean_b = sum(btc_vals) / n
mean_t = sum(tlt_vals) / n
cov = sum((btc_vals[i] - mean_b) * (tlt_vals[i] - mean_t) for i in range(n)) / n
std_b = (sum((x - mean_b)**2 for x in btc_vals) / n) ** 0.5
std_t = (sum((x - mean_t)**2 for x in tlt_vals) / n) ** 0.5
corr = cov / (std_b * std_t)
print(f"{corr:.4f}")
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
