---
name: arrays-data-api-polymarket
description: Calls Polymarket public APIs for prediction market data — discover and search markets/events, real-time and historical pricing (order books, spreads, mid-market prices), user positions and P&L, trade history, on-chain activity, top holders, open interest. Use when the user asks about prediction markets, betting odds, Polymarket prices, order books, price history, market depth, positions, trade history, or market holders.
---


# Arrays Data API — Polymarket

Prediction market discovery, real-time pricing, and analytics via Polymarket public APIs.

## Base URLs and auth

| API | Base URL | Purpose |
|-----|----------|---------|
| Gamma | `https://gamma-api.polymarket.com` | Market discovery, search, metadata |
| CLOB | `https://clob.polymarket.com` | Real-time pricing, order books, price history |
| Data | `https://data-api.polymarket.com` | Analytics, positions, trades, holders |

- **Authentication**: None required. All endpoints are public read-only.
- **NOTE**: This is an external API, NOT behind the Arrays gateway. Do NOT send `X-API-Key` or `ARRAYS_API_KEY` headers.

## Rate limits

| API | Limit |
|-----|-------|
| Gamma | 4,000 req / 10s (`/markets`: 300 / 10s) |
| CLOB | 9,000 req / 10s global; `/book`, `/price`, `/midpoint`, `/spread`: 1,500 / 10s each; `/prices-history`: 1,000 / 10s |
| Data | 1,000 req / 10s |

## Identifiers

Polymarket uses several identifier types (not ticker symbols):

| ID type | Example | Where used |
|---------|---------|------------|
| `id` | `"531202"` | Gamma market/event numeric ID |
| `conditionId` | `"0xb486..."` | On-chain condition identifier (hex) |
| `clobTokenIds` | `"75467..."` (large integer string) | CLOB token ID per outcome — used in all CLOB pricing endpoints |
| `slug` | `"bitboy-convicted"` | URL-friendly market slug |

To get prices for a market: query Gamma `/markets` → extract `clobTokenIds` → use in CLOB endpoints (`/price`, `/midpoint`, `/book`, `/spread`, `/prices-history`).

## Gamma API endpoints (`https://gamma-api.polymarket.com`)

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `/markets` | `markets` | List/filter prediction markets |
| GET | `/events` | `events` | List prediction events (groups of related markets) |
| GET | `/tags` | `tags` | List market tags/categories |
| GET | `/series` | `series` | List market series (recurring events) |
| GET | `/sports` | `sports` | Sports metadata and configuration |
| GET | `/public-search` | `public-search` | Search markets and events by keyword |

## CLOB API endpoints (`https://clob.polymarket.com`)

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `/price` | `price` | Current price for a token (buy or sell side) |
| GET | `/midpoint` | `midpoint` | Mid-market price (best bid + best ask) / 2 |
| GET | `/book` | `book` | Full order book (bids and asks) |
| GET | `/spread` | `spread` | Bid-ask spread |
| GET | `/prices-history` | `prices-history` | Historical price time series |

## Data API endpoints (`https://data-api.polymarket.com`)

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `/positions` | `positions` | User's current open positions (requires `user`) |
| GET | `/closed-positions` | `closed-positions` | User's closed/settled positions (requires `user`) |
| GET | `/trades` | `trades` | Trade history (global or per user) |
| GET | `/activity` | `activity` | User's on-chain activity (requires `user`) |
| GET | `/holders` | `holders` | Top holders for a market |
| GET | `/value` | `value` | Total USD value of user's positions (requires `user`) |
| GET | `/oi` | `oi` | Open interest (global or per market) |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.

## Response format

**Field naming**: Gamma and Data APIs return **camelCase** response fields (e.g. `clobTokenIds`, `outcomePrices`, `volumeNum`, `conditionId`, `proxyWallet`, `transactionHash`). CLOB API uses **snake_case** (e.g. `asset_id`, `min_order_size`). Query parameters use snake_case across all APIs (e.g. `volume_num_min`, `tag_id`).

Polymarket APIs return **raw JSON** — there is no standard wrapper like `{success, response}`. Responses are typically:
- **JSON arrays** for list endpoints (`/markets`, `/events`, `/trades`, etc.)
- **JSON objects** for single-value endpoints (`/price`, `/midpoint`, `/public-search`, etc.)
- **HTTP error codes** with `{"error": "message"}` for errors

## Pagination

All list endpoints use `limit` + `offset` pagination, except `/public-search` which uses `limit_per_type` + `page`. Max per page: **500** (Gamma), **1,000** (`/trades`, `/activity`), **50** (`/public-search`, `/closed-positions`). Only `/public-search` returns `pagination.hasMore` and `totalResults`; for all other endpoints, paginate until the returned array is shorter than `limit`.

Polymarket has tens of thousands of active markets. For screener-type queries, you MUST paginate through all pages — stopping early can miss the vast majority of results. Use server-side filters (`volume_num_min`, `end_date_min/max`, `tag_id`) to reduce data before client-side filtering.

## Python examples

```python
import requests, json, time

GAMMA = "https://gamma-api.polymarket.com"
CLOB  = "https://clob.polymarket.com"
DATA  = "https://data-api.polymarket.com"

# 1. Find top markets and get real-time prices
# Note: Gamma API returns camelCase fields (outcomePrices, volumeNum, clobTokenIds, etc.)
resp = requests.get(f"{GAMMA}/markets", params={
    "active": "true", "closed": "false",
    "order": "volume", "ascending": "false", "limit": 3
})
markets = resp.json()
for m in markets:
    token_ids = json.loads(m["clobTokenIds"])
    outcomes = json.loads(m["outcomes"])
    print(f"\n{m['question']}")
    for i, token_id in enumerate(token_ids):
        p = requests.get(f"{CLOB}/price", params={"token_id": token_id, "side": "buy"})
        print(f"  {outcomes[i]}: {float(p.json()['price']) * 100:.1f}%")

# 2. Search for markets by keyword
resp = requests.get(f"{GAMMA}/public-search", params={"q": "bitcoin", "limit_per_type": 5})
for event in resp.json().get("events", []):
    print(f"{event['title']} — Volume: ${event['volume']:,.0f}")

# 3. Get order book depth
token_id = json.loads(markets[0]["clobTokenIds"])[0]
book = requests.get(f"{CLOB}/book", params={"token_id": token_id}).json()
print(f"Top 3 bids: {book['bids'][:3]}")
print(f"Top 3 asks: {book['asks'][:3]}")

# 4. Get price history (last 1 week)
# Supported intervals: 1h, 6h, 1d, 1w, 1m, max, all
# Omit fidelity for full resolution; avoid small fidelity values
resp = requests.get(f"{CLOB}/prices-history", params={
    "market": token_id, "interval": "1w"
})
history = resp.json()["history"]
for pt in history[-3:]:
    print(f"  t={pt['t']}, price={pt['p']:.4f}")
time.sleep(1)  # space requests to avoid silent empty responses

# 5. Get recent trades
trades = requests.get(f"{DATA}/trades", params={"limit": 10}).json()
for t in trades:
    print(f"{t['side']} {t['size']:.2f} @ {t['price']:.4f} — {t['title']}")

# 6. Get user positions and P&L
user_wallet = "0x60f8b07b6d3cdc1328262ca8382ab6a83836d699"
positions = requests.get(f"{DATA}/positions", params={"user": user_wallet, "limit": 5}).json()
for p in positions:
    print(f"{p['title']} — {p['outcome']}: {p['size']:.2f} shares, PnL: ${p['cashPnl']:.2f}")

# 7. Get top holders for a market
condition_id = markets[0]["conditionId"]
holders = requests.get(f"{DATA}/holders", params={"market": condition_id, "limit": 5}).json()
for token_group in holders:
    for h in token_group["holders"]:
        print(f"  {h.get('name') or h['pseudonym']}: {h['amount']:.2f} shares")
```
