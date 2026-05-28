# X — Handle entity

`GET /api/v1/social-feeds/x/entities/handle/{twitter_handle}`

Retrieve the tracked X/Twitter account profile for a handle. Unlike `by-handle`, this endpoint does NOT auto-create an entity on miss — unknown handles return `NOT_FOUND`.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `twitter_handle` | string | yes | **Path parameter.** Twitter handle (no `@`, case-insensitive) |

#### Response fields

Each item in the `data` array (typically one item):

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

The response envelope also includes `request_id` (no `pagination` block).
