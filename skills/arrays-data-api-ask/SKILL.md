---
name: arrays-data-api-ask
description: Guides the agent to call Arrays REST APIs for market news. Use when the user needs market news articles.
---

# Arrays Data API — Ask (News)

**Domain**: `ask`. Market news.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Path prefix and endpoints

- **Prefix**: `/api/v1/stocks/`
- **Paths** (all GET):
  - `market-news` — market news articles

## Parameters by endpoint

### Market news (`market-news`)

Retrieve market news articles within a specified time range, optionally filtered by symbol. Supports pagination and flexible filtering.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `symbol` | string | no | Stock symbol filter (e.g., AAPL, TSLA) |
| `topic` | string | no | Topic filter. Values: `BLOCKCHAIN`, `EARNINGS`, `ECONOMY_FISCAL`, `ECONOMY_MACRO`, `ECONOMY_MONETARY`, `ENERGY_TRANSPORTATION`, `FINANCE`, `FINANCIAL_MARKETS`, `IPO`, `LIFE_SCIENCES`, `MANUFACTURING`, `MERGERS_AND_ACQUISITIONS`, `REAL_ESTATE`, `RETAIL_WHOLESALE`, `TECHNOLOGY` |
| `source` | string | no | Media source filter. Values: `Reuters`, `AP News`, `BBC`, `The New York Times`, `The Washington Post`, `The Guardian`, `Bloomberg`, `The Wall Street Journal`, `Financial Times`, `CNBC`, `Fortune`, `Forbes`, `TechCrunch`, `MIT Technology Review`, `The Verge`, `WIRED`, `South China Morning Post`, `Nikkei Asia`, `Business Wire`, `PR Newswire` |
| `sort_by_type` | string | no | Sort by type: `PUBLISHED_TIME`, `OVERALL_SENTIMENT_SCORE`, or `RELEVANCE_SCORE` (default: `PUBLISHED_TIME`) |
| `sort_by` | string | no | Sort order: `ASC` or `DESC` (default: `DESC`) |
| `limit` | integer | no | Maximum number of results (1-100, default: 10) |
| `offset` | integer | no | Pagination offset (>=0, default: 0) |

**Response** (V2 format `{ "success": true, "data": { ... } }`):

Top-level `data` fields:

| Field | Type | Description |
|-------|------|-------------|
| `articles` | array | Array of news article objects |
| `totalCount` | int32 | Total number of matching articles |
| `hasMore` | bool | Whether more articles are available |

Each article in `articles`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Article ID |
| `url` | string | Article URL |
| `title` | string | Article title |
| `timePublished` | string | Published time string |
| `publishTime` | int64 | Published time (Unix timestamp) |
| `summary` | string | Article summary |
| `bannerImage` | string | Banner image URL |
| `source` | string | Media source name |
| `categoryWithinSource` | string | Category within the source |
| `sourceDomain` | string | Source domain |
| `authors` | string[] | List of author names |
| `overallSentimentScore` | float64 | Overall sentiment score |
| `overallSentimentLabel` | string | Overall sentiment label |
| `topics` | array | Array of `{ topic: string, relevanceScore: string }` |
| `tickers` | array | Array of `{ ticker: string, relevanceScore: string, tickerSentimentScore: string, tickerSentimentLabel: string }` |

## Example

```js
const base = process.env.ARRAYS_API_BASE || 'https://data-gateway.prd.space.id';
const apiKey = process.env.ARRAYS_API_KEY;
const res = await fetch(`${base}/api/v1/stocks/market-news?start_time=1704067200&end_time=1735689600&symbol=AAPL&limit=10`, {
  headers: { 'X-API-Key': apiKey },
});
const data = await res.json();
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
