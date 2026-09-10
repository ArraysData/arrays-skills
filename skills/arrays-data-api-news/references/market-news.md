# Market news

`GET /api/v1/stocks/market-news`

Retrieve market news articles within a specified time range, optionally filtered by symbol. Supports pagination and flexible filtering.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `symbol` | string | no | Stock symbol filter (e.g., AAPL, TSLA) |
| `topic` | string | no | Topic filter, lowercase: `blockchain`, `earnings`, `economy_fiscal`, `economy_macro`, `economy_monetary`, `energy_and_transportation`, `finance`, `financial_markets`, `ipo`, `life_sciences`, `manufacturing`, `mergers_and_acquisitions`, `real_estate_and_construction`, `retail_and_wholesale`, `technology`. Deprecated aliases `energy_transportation`, `real_estate`, `retail_wholesale` are still accepted and resolve to the values above; `topics[].topic` in responses always carries the canonical form |
| `source` | string | no | Media source filter. Values: `Reuters`, `AP News`, `BBC`, `The New York Times`, `The Washington Post`, `The Guardian`, `Bloomberg`, `The Wall Street Journal`, `Financial Times`, `CNBC`, `Fortune`, `Forbes`, `TechCrunch`, `MIT Technology Review`, `The Verge`, `WIRED`, `South China Morning Post`, `Nikkei Asia`, `Business Wire`, `PR Newswire` |
| `sort_by_type` | string | no | Sort by type: `PUBLISHED_TIME`, `OVERALL_SENTIMENT_SCORE`, or `RELEVANCE_SCORE` (default: `PUBLISHED_TIME`) |
| `sort_by` | string | no | Sort order: `ASC` or `DESC` (default: `DESC`) |
| `limit` | integer | no | Maximum number of results (1-100, default: 10) |
| `offset` | integer | no | Pagination offset (>=0, default: 0) |

**Response envelope:** `{ "success": true, "request_id": "...", "data": [ ... ] }`

Each object in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Article ID |
| `url` | string | Article URL |
| `title` | string | Article title |
| `time_published` | string | Published time string |
| `publish_time` | int64 | Published time (Unix timestamp) |
| `summary` | string | Article summary |
| `banner_image` | string | Banner image URL |
| `source` | string | Media source name |
| `category_within_source` | string | Category within the source |
| `source_domain` | string | Source domain |
| `authors` | string[] | List of author names |
| `overall_sentiment_score` | float64 | Overall sentiment score |
| `overall_sentiment_label` | string | Overall sentiment label |
| `topics` | array | Array of `{ topic: string, relevance_score: string }` |
| `tickers` | array | Array of `{ ticker: string, relevance_score: string, ticker_sentiment_score: string, ticker_sentiment_label: string }` |
