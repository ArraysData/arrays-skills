---
name: arrays-data-api-polymarket-markets
description: Calls Polymarket public APIs for prediction market discovery and analytics — list/search/filter prediction markets and events, tags, series, sports metadata, user positions and P&L, trade history, on-chain activity, top holders, open interest. Use when the user asks about prediction markets, event outcomes, betting odds, Polymarket market data, prediction market positions, trade history, or market holders.
---

# Arrays Data API — Polymarket Markets and Analytics

Prediction market discovery (markets, events, search, tags, series) and user/market analytics (positions, trades, activity, holders, open interest) via Polymarket public APIs.

## Base URLs and auth

- **Gamma API**: `https://gamma-api.polymarket.com` — market discovery, search, metadata
- **Data API**: `https://data-api.polymarket.com` — analytics, positions, trades, holders
- **Authentication**: None required. All endpoints are public read-only.
- **NOTE**: This is an external API, NOT behind the Arrays gateway. Do NOT send `X-API-Key` or `ARRAYS_API_KEY` headers.

## Rate limits

- Gamma API: 4,000 requests / 10 seconds (`/markets`: 300 / 10 seconds)
- Data API: 1,000 requests / 10 seconds

## Identifiers

Polymarket uses several identifier types (not ticker symbols):

| ID type | Example | Where used |
|---------|---------|------------|
| `id` | `"531202"` | Gamma market/event numeric ID |
| `conditionId` | `"0xb486..."` | On-chain condition identifier (hex) |
| `clob_token_ids` | `"75467..."` (large integer string) | CLOB token ID per outcome — use in pricing skill and for filtering markets |
| `slug` | `"bitboy-convicted"` | URL-friendly market slug |

To get prices for a market, extract `clobTokenIds` from the Gamma `/markets` response, then use the `arrays-data-api-polymarket-pricing` skill.

## Endpoints

### Gamma API (`https://gamma-api.polymarket.com`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/markets` | List/filter prediction markets |
| GET | `/events` | List prediction events (groups of related markets) |
| GET | `/tags` | List market tags/categories |
| GET | `/series` | List market series (recurring events) |
| GET | `/sports` | Sports metadata and configuration |
| GET | `/public-search` | Search markets and events by keyword |

### Data API (`https://data-api.polymarket.com`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/positions` | User's current open positions (requires `user`) |
| GET | `/closed-positions` | User's closed/settled positions (requires `user`) |
| GET | `/trades` | Trade history (global or per user) |
| GET | `/activity` | User's on-chain activity (requires `user`) |
| GET | `/holders` | Top holders for a market |
| GET | `/value` | Total USD value of user's positions (requires `user`) |
| GET | `/oi` | Open interest (global or per market) |

## Parameters and response fields by endpoint

### Markets (`/markets`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |
| `order` | string | no | Sort field (e.g. `volume_num`, `liquidity_num`, `created_at`) |
| `ascending` | bool | no | Sort direction |
| `id` | string | no | Filter by market ID |
| `slug` | string | no | Filter by slug |
| `clob_token_ids` | string | no | Filter by CLOB token IDs |
| `condition_ids` | string | no | Filter by condition IDs |
| `question_ids` | string | no | Filter by question IDs |
| `active` | bool | no | Filter active markets |
| `closed` | bool | no | Filter closed markets |
| `archived` | bool | no | Filter archived markets |
| `tag_id` | int | no | Filter by tag ID |
| `related_tags` | string | no | Filter by related tags |
| `liquidity_num_min` | number | no | Min liquidity |
| `liquidity_num_max` | number | no | Max liquidity |
| `volume_num_min` | number | no | Min volume |
| `volume_num_max` | number | no | Max volume |
| `start_date_min` | string | no | Min start date (ISO 8601) |
| `start_date_max` | string | no | Max start date (ISO 8601) |
| `end_date_min` | string | no | Min end date (ISO 8601) |
| `end_date_max` | string | no | Max end date (ISO 8601) |

**Response** — JSON array of market objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Market ID |
| `question` | string | Market question text |
| `conditionId` | string | On-chain condition ID (hex) |
| `slug` | string | URL slug |
| `description` | string | Full market description |
| `outcomes` | string | JSON-encoded array of outcome names, e.g. `"[\"Yes\", \"No\"]"` |
| `outcomePrices` | string | JSON-encoded array of prices, e.g. `"[\"0.2165\", \"0.7835\"]"` |
| `clobTokenIds` | string | JSON-encoded array of CLOB token IDs per outcome |
| `active` | bool | Whether market is active |
| `closed` | bool | Whether market is closed |
| `volume` | string | Total volume (string) |
| `volumeNum` | number | Total volume (number) |
| `liquidity` | string | Current liquidity (string) |
| `liquidityNum` | number | Current liquidity (number) |
| `volume24hr` | number | 24-hour volume |
| `volume1wk` | number | 1-week volume |
| `volume1mo` | number | 1-month volume |
| `volume1yr` | number | 1-year volume |
| `startDate` | string | Market start date (ISO 8601) |
| `endDate` | string | Market end date (ISO 8601) |
| `startDateIso` | string | Start date (YYYY-MM-DD) |
| `endDateIso` | string | End date (YYYY-MM-DD) |
| `image` | string | Market image URL |
| `icon` | string | Market icon URL |
| `featured` | bool | Whether market is featured |
| `new` | bool | Whether market is new |
| `archived` | bool | Whether market is archived |
| `restricted` | bool | Whether market is restricted |
| `negRisk` | bool | Whether market uses neg-risk framework |
| `acceptingOrders` | bool | Whether order book is accepting orders |
| `enableOrderBook` | bool | Whether order book is enabled |
| `orderPriceMinTickSize` | number | Minimum price tick size |
| `orderMinSize` | number | Minimum order size |
| `resolutionSource` | string | Source for market resolution |
| `createdAt` | string | Creation timestamp (ISO 8601) |
| `updatedAt` | string | Last update timestamp (ISO 8601) |
| `events` | array | Associated event objects |

### Events (`/events`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |
| `order` | string | no | Sort field |
| `ascending` | bool | no | Sort direction |
| `id` | string | no | Filter by event ID |
| `slug` | string | no | Filter by slug |
| `tag_id` | int | no | Filter by tag ID |
| `tag_slug` | string | no | Filter by tag slug |
| `active` | bool | no | Filter active events |
| `closed` | bool | no | Filter closed events |
| `archived` | bool | no | Filter archived events |
| `featured` | bool | no | Filter featured events |
| `liquidity_min` | number | no | Min liquidity |
| `liquidity_max` | number | no | Max liquidity |
| `volume_min` | number | no | Min volume |
| `volume_max` | number | no | Max volume |
| `start_date_min` | string | no | Min start date (ISO 8601) |
| `start_date_max` | string | no | Max start date (ISO 8601) |
| `end_date_min` | string | no | Min end date (ISO 8601) |
| `end_date_max` | string | no | Max end date (ISO 8601) |

**Response** — JSON array of event objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Event ID |
| `ticker` | string | Event ticker/slug identifier |
| `slug` | string | URL slug |
| `title` | string | Event title |
| `description` | string | Full event description |
| `resolutionSource` | string | Source URL for resolution |
| `startDate` | string | Start date (ISO 8601) |
| `creationDate` | string | Creation date (ISO 8601) |
| `endDate` | string | End date (ISO 8601) |
| `image` | string | Event image URL |
| `icon` | string | Event icon URL |
| `active` | bool | Whether event is active |
| `closed` | bool | Whether event is closed |
| `archived` | bool | Whether event is archived |
| `featured` | bool | Whether event is featured |
| `restricted` | bool | Whether event is restricted |
| `category` | string | Event category (e.g. `"Sports"`, `"Politics"`) |
| `liquidity` | number | Current liquidity |
| `volume` | number | Total volume |
| `openInterest` | number | Open interest |
| `volume24hr` | number | 24-hour volume |
| `volume1wk` | number | 1-week volume |
| `volume1mo` | number | 1-month volume |
| `volume1yr` | number | 1-year volume |
| `commentCount` | number | Number of comments |
| `markets` | array | Array of nested market objects |

### Tags (`/tags`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |
| `order` | string | no | Sort field |
| `ascending` | bool | no | Sort direction |

**Response** — JSON array of tag objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Tag ID |
| `label` | string | Tag display name |
| `slug` | string | URL slug |
| `createdAt` | string | Creation timestamp (ISO 8601) |
| `updatedAt` | string | Last update timestamp (ISO 8601) |

### Series (`/series`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |
| `order` | string | no | Sort field |
| `ascending` | bool | no | Sort direction |
| `slug` | string | no | Filter by slug |
| `closed` | bool | no | Filter closed series |
| `recurrence` | string | no | Filter by recurrence type (e.g. `weekly`) |

**Response** — JSON array of series objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Series ID |
| `ticker` | string | Series ticker |
| `slug` | string | URL slug |
| `title` | string | Series title |
| `seriesType` | string | Type (e.g. `"single"`) |
| `recurrence` | string | Recurrence pattern (e.g. `"weekly"`) |
| `active` | bool | Whether series is active |
| `closed` | bool | Whether series is closed |
| `archived` | bool | Whether series is archived |
| `featured` | bool | Whether series is featured |
| `restricted` | bool | Whether series is restricted |
| `createdAt` | string | Creation timestamp (ISO 8601) |
| `updatedAt` | string | Last update timestamp (ISO 8601) |
| `events` | array | Array of nested event objects |

### Sports (`/sports`)

No request parameters.

**Response** — JSON array of sport config objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Sport ID |
| `sport` | string | Sport code (e.g. `"nba"`, `"epl"`, `"mlb"`) |
| `image` | string | Sport image URL |
| `resolution` | string | Resolution source URL |
| `ordering` | string | Ordering type (e.g. `"home"`) |
| `tags` | string | Comma-separated tag IDs |
| `series` | string | Associated series ID |
| `createdAt` | string | Creation timestamp (ISO 8601) |

### Public search (`/public-search`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `q` | string | **yes** | Search query string |
| `limit_per_type` | int | no | Max results per entity type |
| `page` | int | no | Page number |
| `events_status` | string | no | Filter events by status |
| `events_tag` | string | no | Filter events by tag |
| `sort` | string | no | Sort field |
| `ascending` | bool | no | Sort direction |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `events` | array | Array of matching event objects (same shape as `/events`) |

### Positions (`/positions`)

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

### Closed positions (`/closed-positions`)

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

### Trades (`/trades`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `user` | string | no | Filter by user wallet address |
| `market` | string | no | Filter by conditionId |
| `asset` | string | no | Filter by CLOB token ID |
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |

**Response** — JSON array of trade objects:

| Field | Type | Description |
|-------|------|-------------|
| `proxyWallet` | string | Trader wallet address |
| `side` | string | Trade side: `"BUY"` or `"SELL"` |
| `asset` | string | CLOB token ID |
| `conditionId` | string | Condition ID (hex) |
| `size` | number | Trade size (shares) |
| `price` | number | Execution price |
| `timestamp` | number | Trade timestamp (Unix seconds) |
| `title` | string | Market title |
| `slug` | string | Market slug |
| `icon` | string | Market icon URL |
| `eventSlug` | string | Parent event slug |
| `outcome` | string | Outcome name |
| `outcomeIndex` | number | Outcome index |
| `name` | string | Trader display name |
| `pseudonym` | string | Trader pseudonym |
| `transactionHash` | string | On-chain transaction hash |

### Activity (`/activity`)

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

### Holders (`/holders`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `market` | string | **yes** | Condition ID (hex) |
| `limit` | int | no | Number of top holders per token |

**Response** — JSON array of token-grouped holder objects:

| Field | Type | Description |
|-------|------|-------------|
| `token` | string | CLOB token ID |
| `holders` | array | Array of holder objects |

Each holder object:

| Field | Type | Description |
|-------|------|-------------|
| `proxyWallet` | string | Holder wallet address |
| `asset` | string | CLOB token ID |
| `amount` | number | Number of shares held |
| `outcomeIndex` | number | Outcome index |
| `name` | string | Display name |
| `pseudonym` | string | Pseudonym |
| `verified` | bool | Whether account is verified |

### Value (`/value`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `user` | string | **yes** | User wallet address (proxy wallet) |

**Response** — JSON array with a single object:

| Field | Type | Description |
|-------|------|-------------|
| `user` | string | User wallet address |
| `value` | number | Total portfolio value in USD |

### Open interest (`/oi`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `market` | string | no | Condition ID to filter; omit for global OI |

**Response** — JSON array of OI objects:

| Field | Type | Description |
|-------|------|-------------|
| `market` | string | Market identifier or `"GLOBAL"` |
| `value` | number | Open interest in USD |

## Response format

Polymarket APIs return **raw JSON** — there is no standard wrapper like `{success, response}`. Responses are typically:
- **JSON arrays** for list endpoints (`/markets`, `/events`, `/trades`, etc.)
- **JSON objects** for single-value endpoints (`/public-search` returns `{events: [...]}`)
- **HTTP error codes** with `{"error": "message"}` for errors

Always check the HTTP status code. A `200` indicates success.

## Pagination

All list endpoints support **offset-based pagination** with `limit` and `offset` parameters. There is no cursor-based pagination or `has_more` field — if the returned array length equals `limit`, there may be more results.

## Python examples

```python
import requests, json

GAMMA = "https://gamma-api.polymarket.com"
DATA = "https://data-api.polymarket.com"

# 1. List top prediction markets by volume
resp = requests.get(f"{GAMMA}/markets", params={
    "active": "true",
    "closed": "false",
    "order": "volume_num",
    "ascending": "false",
    "limit": 10
})
markets = resp.json()
for m in markets:
    prices = json.loads(m["outcomePrices"])
    outcomes = json.loads(m["outcomes"])
    print(f"{m['question']}")
    for i, outcome in enumerate(outcomes):
        print(f"  {outcome}: {float(prices[i]) * 100:.1f}%")
    print(f"  Volume: ${m['volumeNum']:,.0f}")

# 2. Search for markets by keyword
resp = requests.get(f"{GAMMA}/public-search", params={
    "q": "bitcoin price",
    "limit_per_type": 5
})
results = resp.json()
for event in results.get("events", []):
    print(f"{event['title']} — Volume: ${event['volume']:,.0f}")

# 3. Get recent trades across all markets
resp = requests.get(f"{DATA}/trades", params={"limit": 20})
trades = resp.json()
for t in trades:
    print(f"{t['side']} {t['size']:.2f} shares of \"{t['outcome']}\" @ {t['price']:.4f} — {t['title']}")

# 4. Get global open interest
resp = requests.get(f"{DATA}/oi")
oi = resp.json()
for item in oi:
    print(f"{item['market']}: ${item['value']:,.2f}")

# 5. Get top holders for a market
market_condition_id = "0xb48621f7eba07b0a3eeabc6afb09ae42490239903997b9d412b0f69aeb040c8b"
resp = requests.get(f"{DATA}/holders", params={
    "market": market_condition_id,
    "limit": 5
})
holders_data = resp.json()
for token_group in holders_data:
    for holder in token_group["holders"]:
        print(f"{holder['name'] or holder['pseudonym']}: {holder['amount']:.2f} shares")

# 6. Get user positions and P&L
user_wallet = "0x60f8b07b6d3cdc1328262ca8382ab6a83836d699"
resp = requests.get(f"{DATA}/positions", params={"user": user_wallet, "limit": 10})
positions = resp.json()
for p in positions:
    print(f"{p['title']} — {p['outcome']}: {p['size']:.2f} shares, PnL: ${p['cashPnl']:.2f} ({p['percentPnl']:.1f}%)")
```
