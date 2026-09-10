# X — Full-text search

`GET /api/v1/social-feeds/x/search`

Elasticsearch full-text search (BM25 over `full_text` with multilingual analyzers) over the tracked-handle registry index — **not** a live X/Twitter search. It reads only already-ingested posts and never fetches on-demand. For a handle that isn't tracked yet, call `POST /api/v1/social-feeds/x/handles` first to start tracking it — the discovery endpoint, which is rate-capped and **billed as a premium discovery unit** (see [x-handles.md](x-handles.md)); until then its posts won't appear here.

**Sort order.** By default it depends on `q`: with `q` present results are BM25-ranked by relevance; with `q` omitted they're reverse-chronological (`published_at` DESC) within the time window. Pass `sort` to force an ordering regardless of `q`:
- `relevance` — BM25 (default when `q` is present)
- `latest` — reverse-chronological (`published_at` DESC); use to get newest-first even with a query
- `hottest` — by `view_count` DESC

**Anti-scrape rule:** when both `q` and `handle` are empty, `since` is capped to the last 30 days (and defaults to 30d if omitted). Passing either `q` or `handle` lifts that cap.

All filters (`q`, `handle`, `since`, `until`, `content_type`, `has_media`) are optional and compose, so the endpoint also works as a pure structured filter (e.g. all `original` posts from a handle in a time window).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `q` | string | no | Search query (BM25 over `full_text`). Tokens like `#tag` route to a hashtag filter clause and `@user` routes to an author filter clause. Omit for reverse-chronological listing (subject to the 30-day window cap above) |
| `handle` | string | no | Restrict to a single handle (no `@`, case-insensitive) |
| `since` | int64 | no | Start time (Unix seconds). Filter to posts at/after this time |
| `until` | int64 | no | End time (Unix seconds). Filter to posts at/before this time |
| `content_type` | array | no | Filter by content type. Values: `original`, `reply`, `retweet`, `quote`. Repeat the query param to pass multiple |
| `has_media` | boolean | no | Only return posts with media when `true` |
| `limit` | integer | no | Max results (default 50, max 200) |
| `offset` | integer | no | Pagination offset (default 0) |
| sort | string | no | Result ordering: relevance (default when q is present), latest (default when q is omitted), or hottest (by view_count DESC) |

#### Response fields

Each item in the `data` array follows the same per-post shape as `by-handle`:

| Field | Type | Description |
|-------|------|-------------|
| `platform_id` | string | Tweet ID on X/Twitter |
| `url` | string | Canonical `x.com` URL |
| `published_at` | string | ISO 8601 (UTC) — original publish time |
| `last_observed_at` | string | ISO 8601 (UTC) — last refresh |
| `first_observed_at` | string | ISO 8601 (UTC) — when Arrays **first ingested** this post (earliest observation). For posts captured via historical backfill this is the backfill run time, **not** the original publish time (use `published_at` for that). Omitted when unavailable |
| `twitter_handle` | string | Author's handle |
| `display_name` | string | Author's display name |
| `full_text` | string | Post text |
| `content_type` | string | `original`, `reply`, `retweet`, or `quote` |
| `meta_json` | string | Stringified JSON: full X API metadata (`author_id`, `conversation_id`, `public_metrics`, `retweeted_post_id` or `quoted_post_id`, etc.). Parse with `JSON.parse` |
| `media_json` | string | Stringified JSON array of attached media |
| `like_count` | int64 | Likes. Omitted when unknown; genuine `0` is included |
| `retweet_count` | int64 | Retweets. Omitted when unknown; genuine `0` is included |
| `reply_count` | int64 | Replies. Omitted when unknown; genuine `0` is included |
| `view_count` | int64 | Impressions. Omitted when unknown; genuine `0` is included |
| `quote_count` | int64 | Quote tweets. Omitted when unknown; genuine `0` is included |
| `bookmark_count` | int64 | Bookmarks. Omitted when unknown; genuine `0` is included |
| `conversation_id` | string | X conversation thread the post belongs to |
| `in_reply_to_user_id` | string | If a reply, the user ID being replied to |
| `referenced_tweets` | array | One entry per referenced tweet. Each item: `{id, type, author_external_id?, text?, published_at?, author_handle?, author_display_name?}` where `type` is `replied_to` / `retweeted` / `quoted`; `author_external_id` is the referenced author's X numeric user ID when known (empty on legacy rows pre-backfill); `text`, `published_at` (RFC 3339) and the author fields are present when the referenced post has been ingested |
| `source` | object | **Nested source tweet** for `retweet` / `quote` / `reply` posts — a tweet object with `twitter_handle` / `display_name` / `full_text` / counters / `media` (each media item: `type`, `url`, `media_key`, `width`, `height`). Omitted when `content_type` is `original` |
| `mentions` | string[] | Handles mentioned (no `@`) |
| `entity_mentions.people` | array | Linked person entities |
| `entity_mentions.tickers` | array | Linked ticker entities |
| `entity_mentions.topics` | array | Linked topic entities |

The response envelope also includes `pagination: { limit, offset }` and `request_id`.
