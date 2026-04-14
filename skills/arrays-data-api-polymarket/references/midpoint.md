# Midpoint

`GET midpoint`

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
