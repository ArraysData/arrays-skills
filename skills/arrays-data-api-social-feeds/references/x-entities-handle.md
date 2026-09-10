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
| `last_synced_at` | string | ISO 8601 (UTC) — when Arrays last synced this handle's posts (the upper bound of post coverage). Stays current while the handle is actively tracked; for a handle no longer tracked it marks when syncing stopped; omitted if the handle has never been synced. This is a *sync* timestamp, not a guarantee that every post before this time is present. |
| `tags` | object | **Optional** — present when the account has been classified |

`tags` sub-fields:

| Field | Type | Description |
|-------|------|-------------|
| `tags.account_kind` | string | `personal` or `institution` |
| `tags.occupation` | string[] | Roles (e.g. `investing_kol`, `investor`, `builder`). Populated only when `account_kind == "personal"` |
| `tags.institution_type` | string | E.g. `company`, `government`, `media`. Populated only when `account_kind == "institution"` |
| `tags.topics` | string[] | Topic tags (e.g. `crypto`, `ai`, `policy`, `entertainment`) |
| `tags.language` | string[] | ISO language codes (e.g. `en`, `ko`) |
| `tags.behavior` | string[] | Posting-behavior tags (e.g. `original`, `curator`, `aggregator`) |

The response envelope also includes `request_id` (no `pagination` block).
