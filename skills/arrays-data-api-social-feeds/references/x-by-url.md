# X — Post by URL

`GET /api/v1/social-feeds/x/by-url`

Fetch a single post by its canonical `x.com` / `twitter.com` URL.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | yes | Canonical `x.com` or `twitter.com` tweet URL |

#### Response fields

The `data` array contains a single post object with the same per-post shape returned by `by-handle`. Sparsely-observed tweets may have a reduced field set — `meta_json`, `media_json`, `view_count`, `quote_count`, `bookmark_count`, `mentions`, and conversation/reply metadata can be absent when the record hasn't been enriched yet.

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Internal record ID |
| `source_type` | string | Always `twitter` |
| `platform_id` | string | Tweet ID on X/Twitter |
| `url` | string | Canonical `x.com` URL |
| `published_at` | string | ISO 8601 (UTC) — original publish time |
| `last_observed_at` | string | ISO 8601 (UTC) — last refresh |
| `version` | int32 | Internal version counter |
| `twitter_handle` | string | Author's handle |
| `display_name` | string | Author's display name |
| `full_text` | string | Post text |
| `content_type` | string | `original`, `reply`, `retweet`, or `quote` |
| `meta_json` | string | Stringified JSON: full X API metadata (`author_id`, `conversation_id`, `public_metrics`, `retweeted_post_id`, etc.). Parse with `JSON.parse`. May be absent on sparsely-observed posts |
| `media_json` | string | Stringified JSON array of attached media. May be absent |
| `revisions_json` | string | Stringified JSON array of edit history |
| `like_count` | int64 | Likes |
| `retweet_count` | int64 | Retweets |
| `reply_count` | int64 | Replies |
| `view_count` | int64 | Impressions. May be absent |
| `quote_count` | int64 | Quote tweets. May be absent |
| `bookmark_count` | int64 | Bookmarks. May be absent |
| `conversation_id` | string | X conversation thread. May be absent |
| `in_reply_to_user_id` | string | If a reply, the user ID being replied to. May be absent |
| `referenced_tweet_id` | string | If reply/retweet/quote, the referenced tweet ID. May be absent |
| `referenced_tweet_type` | string | `replied_to`, `retweeted`, or `quoted`. May be absent |
| `mentions` | string[] | Handles mentioned (no `@`). May be absent |
| `entity_mentions.people` | array | Linked person entities |
| `entity_mentions.tickers` | array | Linked ticker entities |
| `entity_mentions.topics` | array | Linked topic entities |

The response envelope also includes `request_id` (no `pagination` block — this endpoint always returns a single post).
