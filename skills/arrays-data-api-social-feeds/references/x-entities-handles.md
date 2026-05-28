# X — List tracked handles

`GET /api/v1/social-feeds/x/entities/handles`

Paginated list of currently tracked X/Twitter accounts, sorted by `followers_count` DESC.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | integer | no | Max results (default 50, max 200) |
| `offset` | integer | no | Pagination offset (default 0) |

#### Response fields

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `twitter_id` | string | X/Twitter numeric user ID |
| `twitter_handle` | string | Account handle (lowercased) |
| `twitter_display_name` | string | Display name |
| `description` | string | Profile bio |
| `followers_count` | int64 | Follower count |
| `following_count` | int64 | Following count |
| `verified` | boolean | Verified badge |
| `verified_type` | string | Type of verification (e.g. `blue`, `business`, `government`) |
| `profile_image_url` | string | URL of the account's avatar image |
| `profile_banner_url` | string | URL of the account's banner image |
| `account_created_at` | string | ISO 8601 (UTC) — account creation time |
| `earliest_backfilled_at` | string | ISO 8601 (UTC) — start of contiguous post coverage. Older posts may exist (e.g. pulled in via URL lookups, or as replies/retweets to other tweets) but aren't guaranteed contiguous before this time. |

The response envelope also includes `pagination: { limit, offset }` and `request_id`.
