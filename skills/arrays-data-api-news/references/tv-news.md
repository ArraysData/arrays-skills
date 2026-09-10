# Wire news

`GET /api/v1/stocks/tv-news`

Wire news stories (Dow Jones, Reuters, Stocktwits, MarketWatch), newest first. US and non-US symbols. Coverage from 2026-07-03.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds) |
| `symbol` | string | no | Canonical symbol filter, case-insensitive (`AAPL`, `BRK.B`, `0700.HK`, `1433.T`). Mutually exclusive with `industry` |
| `industry` | string | no | Industry name, the same taxonomy as `company/detail` `industry`; exact match including case (`Semiconductors`, `Banks - Diversified`, `Apparel - Retail`). A misspelled value returns an empty array. Mutually exclusive with `symbol` |
| `limit` | int32 | no | Max results (1–500, default 10). Set explicitly when collecting complete results; no offset |

If the returned count equals `limit`, split the time window and repeat until each subwindow returns fewer than `limit` stories. Deduplicate boundary overlaps by `story_id`. A one-hour window or a symbol/industry filter does not guarantee completeness. If the smallest supported window still reaches the limit, report that completeness cannot be verified.

**Response envelope:** `{ "success": true, "request_id": "...", "data": [ ... ] }`

Each object in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `story_id` | string | Story ID, prefixed by provider |
| `title` | string | Headline |
| `content` | string | Story text; empty for roughly one story in five |
| `published_at` | int64 | Published time (Unix seconds) |
| `provider` | string | `dow-jones`, `reuters`, `stocktwits` or `market-watch` |
| `story_url` | string | Public permalink to the story; the full text is already in `content` |
| `symbols` | string[] | Canonical symbols tagged on the story; empty for roughly one story in five |
| `industries` | string[] | Industry names of the tagged symbols, same taxonomy as `company/detail` `industry` |
