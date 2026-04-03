---
name: arrays-data-api-polymarket-pricing
description: Calls Polymarket CLOB (Central Limit Order Book) public API for prediction market pricing — token prices, mid-market prices, order books, bid-ask spreads, price history for prediction markets. Use when the user asks about Polymarket prices, prediction market odds, order books, price history, bid-ask spreads, or market depth.
---

# Arrays Data API — Polymarket Pricing

Real-time and historical pricing for prediction market outcome tokens via the Polymarket CLOB API — prices, mid-market prices, order books, spreads, and price history.

## Base URL and auth

- **Base**: `https://clob.polymarket.com`
- **Authentication**: None required. All endpoints are public read-only.
- **NOTE**: This is an external API, NOT behind the Arrays gateway. Do NOT send `X-API-Key` or `ARRAYS_API_KEY` headers.

## Rate limits

- 9,000 requests / 10 seconds

## Identifiers

Pricing endpoints use **CLOB token IDs** — large integer strings that identify a specific outcome token. Each prediction market has two tokens (one per outcome, e.g. "Yes" and "No").

To obtain token IDs: query `GET /markets` on the Gamma API (via `arrays-data-api-polymarket-markets` skill) and extract the `clobTokenIds` field (JSON-encoded array).

The `/prices-history` endpoint uses a **token ID** as its `market` parameter (not a conditionId).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/price` | Current price for a single outcome token |
| GET | `/midpoint` | Mid-market price for a single token |
| GET | `/book` | Full order book (bids and asks) for a token |
| GET | `/spread` | Bid-ask spread for a token |
| GET | `/prices-history` | Historical price time series |
| GET | `/time` | Server time (Unix timestamp) |
| GET | `/ok` | Health check |

## Parameters and response fields by endpoint

### Price (`/price`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token_id` | string | **yes** | CLOB token ID |
| `side` | string | **yes** | `"buy"` or `"sell"` |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `price` | string | Current price (decimal string, e.g. `"0.216"`) |

### Midpoint (`/midpoint`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token_id` | string | **yes** | CLOB token ID |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `mid` | string | Mid-market price (decimal string, e.g. `"0.218"`) |

### Price types across Polymarket APIs

| Price source | API | Meaning | Latency | Matches website? |
|-------------|-----|---------|---------|-----------------|
| `outcomePrices` | Gamma `/markets`, `/events` | Cached midpoint snapshot | Minutes (delayed) | ~0.1–0.5% lower |
| `/midpoint` | CLOB | Real-time (Best Bid + Best Ask) / 2 | Real-time | ~half a spread lower |
| `/price?side=buy` | CLOB | Real-time Ask (cost to buy) | Real-time | **= website displayed price** |
| `/price?side=sell` | CLOB | Real-time Bid (proceeds from selling) | Real-time | One spread lower |

**Guidance**: When the user asks for "current price" or "odds", use `/price?side=buy` to match what they see on the Polymarket website. Use `/midpoint` for unbiased mid-market estimates. The Gamma `outcomePrices` field is convenient for bulk screening but may be stale.

### Order book (`/book`)

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

### Spread (`/spread`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token_id` | string | **yes** | CLOB token ID |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `spread` | string | Bid-ask spread (decimal string, e.g. `"0.004"`) |

### Price history (`/prices-history`)

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `market` | string | **yes** | CLOB **token ID** (not conditionId) |
| `interval` | string | no | Time range: `1h`, `6h`, `1d`, `1w`, `1m`. Only these five values are accepted; others (e.g. `3m`, `6m`, `1y`, `max`) return 400 errors. |
| `fidelity` | int | no | Sampling interval in minutes (e.g. fidelity=5 means one data point every 5 minutes, fidelity=60 means one per hour). Omit for full-resolution data. Avoid very small values as the API may return an empty `history` array silently. |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `history` | array | Array of price data points |

Each data point:

| Field | Type | Description |
|-------|------|-------------|
| `t` | number | Unix timestamp (seconds) |
| `p` | number | Price at that time |

**Rate-limit note**: Rapid consecutive `/prices-history` requests may return HTTP 200 with an empty `history` array (silent failure, no error code). Space requests at least 1 second apart to avoid this.

### Server time (`/time`)

No request parameters.

**Response** — plain number (Unix timestamp in seconds).

### Health check (`/ok`)

No request parameters.

**Response** — plain JSON string: `"OK"`.

## Response format

Polymarket CLOB API returns **raw JSON** — there is no standard wrapper. Each endpoint has its own response shape as documented above. HTTP status `200` indicates success. Errors return non-200 status codes with `{"error": "message"}`.

## Python examples

```python
import requests, json

CLOB = "https://clob.polymarket.com"
GAMMA = "https://gamma-api.polymarket.com"

# Step 1: Find a market and extract token IDs
resp = requests.get(f"{GAMMA}/markets", params={
    "active": "true", "closed": "false",
    "order": "volume_num", "ascending": "false", "limit": 1
})
market = resp.json()[0]
token_ids = json.loads(market["clobTokenIds"])
outcomes = json.loads(market["outcomes"])
print(f"Market: {market['question']}")
print(f"Outcomes: {outcomes}")
print(f"Token IDs: {token_ids}")

# Step 2: Get current prices for each outcome
for i, token_id in enumerate(token_ids):
    resp = requests.get(f"{CLOB}/price", params={
        "token_id": token_id, "side": "buy"
    })
    price = resp.json()["price"]
    print(f"  {outcomes[i]}: {float(price) * 100:.1f}% (buy)")

# 3. Get mid-market price
resp = requests.get(f"{CLOB}/midpoint", params={"token_id": token_ids[0]})
mid = resp.json()["mid"]
print(f"Midpoint: {float(mid) * 100:.1f}%")

# 4. Get bid-ask spread
resp = requests.get(f"{CLOB}/spread", params={"token_id": token_ids[0]})
spread = resp.json()["spread"]
print(f"Spread: {float(spread) * 100:.2f}%")

# 5. Get order book depth
resp = requests.get(f"{CLOB}/book", params={"token_id": token_ids[0]})
book = resp.json()
print(f"Top 3 bids:")
for b in book["bids"][:3]:
    print(f"  {b['price']} x {b['size']}")
print(f"Top 3 asks:")
for a in book["asks"][:3]:
    print(f"  {a['price']} x {a['size']}")

# 6. Get price history (last 1 week)
# Supported intervals: 1h, 6h, 1d, 1w, 1m
# Omit fidelity for full resolution; avoid small fidelity values
resp = requests.get(f"{CLOB}/prices-history", params={
    "market": token_ids[0],
    "interval": "1w"
})
history = resp.json()["history"]
print(f"Price history ({len(history)} points):")
for point in history[-5:]:
    print(f"  t={point['t']}, price={point['p']:.4f}")
```
