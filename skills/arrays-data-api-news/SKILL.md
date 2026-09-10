---
name: arrays-data-api-news
description: Calls Arrays REST APIs for news — market news with sentiment scores and topic tags (market-news), and a high-volume wire news stream from Dow Jones, Reuters, Stocktwits and MarketWatch with per-story symbols and industries (tv-news). Use when the user asks for news about a stock, a sector or industry, a topic such as earnings or IPOs, news sentiment, or the latest headlines.
---


# Arrays Data API — News

**Domain**: `news`. Two news feeds with different sources, depth and volume.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.arrays.org`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Endpoints

- **Prefix**: `/api/v1/stocks/`

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `market-news` | `market-news` | Market news with sentiment scores, topic and source filters, sortable, offset paging |
| GET | `tv-news` | `tv-news` | Wire news stream (Dow Jones, Reuters, Stocktwits, MarketWatch) with `symbols` and `industries`; US and non-US symbols |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.

## Choosing an endpoint

- **Sentiment, topic (earnings / IPO / M&A …), or a named outlet** → `market-news`. The only feed with sentiment scores and `offset` paging.
- **Breaking headlines, a non-US symbol (`0700.HK`, `1433.T`), or an industry** → `tv-news`. Wire volume (thousands of stories a day); coverage since 2026-07-03.

## Important notes

- **Time window**: both take `start_time` / `end_time` as Unix seconds and return newest first.
- **Complete results from `tv-news`**: there is no `offset`. Set `limit` explicitly (up to 500). If the number of returned stories equals `limit`, treat the window as potentially truncated and split it into smaller time windows, repeating until each returns fewer than `limit` stories. Deduplicate boundary overlaps by `story_id`. A one-hour window or a symbol/industry filter does not guarantee completeness; if even the smallest supported window reaches the limit, report that completeness cannot be verified.
- **Symbols**: `tv-news` takes the arrays canonical symbol (`AAPL`, `BRK.B`, `0700.HK`), case-insensitive; `market-news` takes US symbols.
- **Empty results** are `200` with `"data": []`, including for an unknown symbol.

## Example

```js
const base = process.env.ARRAYS_API_BASE_URL || 'https://data-tools.prd.arrays.org';
const apiKey = process.env.ARRAYS_API_KEY;
const now = Math.floor(Date.now() / 1000);

// Sentiment-tagged market news for AAPL
let res = await fetch(`${base}/api/v1/stocks/market-news?start_time=${now - 7 * 86400}&end_time=${now}&symbol=AAPL&limit=10`, {
  headers: { 'X-API-Key': apiKey },
});
let data = await res.json();

// Last hour of wire headlines for the semiconductor industry
res = await fetch(`${base}/api/v1/stocks/tv-news?start_time=${now - 3600}&end_time=${now}&industry=Semiconductors&limit=100`, {
  headers: { 'X-API-Key': apiKey },
});
data = await res.json();
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
