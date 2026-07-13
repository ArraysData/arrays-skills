# X — Post by URL

`GET /api/v1/social-feeds/x/by-url`

Fetch a single post by its canonical `x.com` / `twitter.com` URL.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | yes | Canonical `x.com` or `twitter.com` tweet URL |

#### Response fields

The `data` array contains a single post object with the same per-post shape returned by `by-handle`. Sparsely-observed tweets may have a reduced field set — `meta_json`, `media_json`, the counter fields (`view_count` / `quote_count` / `bookmark_count` / etc.), `mentions`, and conversation/reply metadata can be absent when the record hasn't been enriched yet. The `first_observed_at` field (returned by `by-handle` / `search`) is **not** returned by this endpoint.

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `platform_id` | string | Tweet ID on X/Twitter |
| `url` | string | Canonical `x.com` URL |
| `published_at` | string | ISO 8601 (UTC) — original publish time |
| `last_observed_at` | string | ISO 8601 (UTC) — last refresh |
| `twitter_handle` | string | Author's handle |
| `display_name` | string | Author's display name |
| `full_text` | string | Post text |
| `content_type` | string | `original`, `reply`, `retweet`, or `quote` |
| `meta_json` | string | Stringified JSON: full X API metadata (`author_id`, `conversation_id`, `public_metrics`, `retweeted_post_id`, etc.). Parse with `JSON.parse`. May be absent on sparsely-observed posts |
| `media_json` | string | Stringified JSON array of attached media. May be absent |
| `like_count` | int64 | Likes. Omitted when unknown; genuine `0` is included |
| `retweet_count` | int64 | Retweets. Omitted when unknown; genuine `0` is included |
| `reply_count` | int64 | Replies. Omitted when unknown; genuine `0` is included |
| `view_count` | int64 | Impressions. Omitted when unknown; genuine `0` is included |
| `quote_count` | int64 | Quote tweets. Omitted when unknown; genuine `0` is included |
| `bookmark_count` | int64 | Bookmarks. Omitted when unknown; genuine `0` is included |
| `conversation_id` | string | X conversation thread. May be absent |
| `in_reply_to_user_id` | string | If a reply, the user ID being replied to. May be absent |
| `referenced_tweets` | array | One entry per referenced tweet. Each item: `{id, type, author_external_id?}` where `type` is `replied_to` / `retweeted` / `quoted`, and `author_external_id` is the referenced author's X numeric user ID when known (empty on legacy rows pre-backfill). May be absent on sparsely-observed posts |
| `source` | object | **Nested source tweet** for `retweet` / `quote` / `reply` posts — a tweet object with `twitter_handle` / `display_name` / `full_text` / counters / `media`. Omitted when `content_type` is `original` or when the source can't be hydrated |
| `mentions` | string[] | Handles mentioned (no `@`). May be absent |
| `entity_mentions.people` | array | Linked person entities |
| `entity_mentions.tickers` | array | Linked ticker entities |
| `entity_mentions.topics` | array | Linked topic entities |

The response envelope also includes `request_id` (no `pagination` block — this endpoint always returns a single post).
