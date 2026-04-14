---
name: arrays-data-api-ask
description: Guides the agent to call Arrays REST APIs for market news. Use when the user needs market news articles.
---


# Arrays Data API — Ask (News)

**Domain**: `ask`. Market news.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Path prefix and endpoints

- **Prefix**: `/api/v1/stocks/`
- **Paths** (all GET):
  - `market-news` — market news articles

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `market-news` | `market-news` | Market news |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Example

```js
const base = process.env.ARRAYS_API_BASE_URL || 'https://data-tools.prd.space.id';
const apiKey = process.env.ARRAYS_API_KEY;
const res = await fetch(`${base}/api/v1/stocks/market-news?start_time=1704067200&end_time=1735689600&symbol=AAPL&limit=10`, {
  headers: { 'X-API-Key': apiKey },
});
const data = await res.json();
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
