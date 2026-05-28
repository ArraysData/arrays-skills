# X — Posts by handle

`GET /api/v1/social-feeds/x/by-handle`

Paginated list of posts from the given X/Twitter handle, sorted by `published_at` DESC. Unknown handles trigger an on-demand X API lookup; the first page is returned synchronously and full historical backfill happens in the background once anti-abuse thresholds (followers + age) are satisfied.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `twitter_handle` | string | yes | Twitter handle (no `@`, case-insensitive) |
| `since` | int64 | no | Start time (Unix seconds). Filter to posts at/after this time |
| `until` | int64 | no | End time (Unix seconds). Filter to posts at/before this time |
| `content_type` | array | no | Filter by content type. Values: `original`, `reply`, `retweet`, `quote`. Repeat the query param to pass multiple |
| `has_media` | boolean | no | Only return posts with media when `true` |
| `limit` | integer | no | Max results (default 50, max 200) |
| `offset` | integer | no | Pagination offset (default 0) |

#### Response fields

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
| `meta_json` | string | Stringified JSON: full X API metadata (`author_id`, `conversation_id`, `public_metrics`, `retweeted_post_id`, etc.). Parse with `JSON.parse` |
| `media_json` | string | Stringified JSON array of attached media |
| `revisions_json` | string | Stringified JSON array of edit history |
| `like_count` | int64 | Likes |
| `retweet_count` | int64 | Retweets |
| `reply_count` | int64 | Replies |
| `view_count` | int64 | Impressions |
| `quote_count` | int64 | Quote tweets |
| `bookmark_count` | int64 | Bookmarks |
| `conversation_id` | string | X conversation thread the post belongs to |
| `in_reply_to_user_id` | string | If a reply, the user ID being replied to |
| `referenced_tweet_id` | string | If reply/retweet/quote, the referenced tweet ID |
| `referenced_tweet_type` | string | `replied_to`, `retweeted`, or `quoted` |
| `mentions` | string[] | Handles mentioned (no `@`) |
| `entity_mentions.people` | array | Linked person entities |
| `entity_mentions.tickers` | array | Linked ticker entities |
| `entity_mentions.topics` | array | Linked topic entities |

The response envelope also includes `pagination: { limit, offset }` and `request_id`.
