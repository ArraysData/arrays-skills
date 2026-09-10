# Podcast — Shows

`GET /api/v1/other/podcast/shows`

Show catalog, paginated. All parameters optional.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | no | Show name, case-insensitive exact match |
| `podcast_show_id` | int64 | no | Exact show id |
| `limit` | integer | no | Max results (1–200, default 10) |
| `offset` | integer | no | Pagination offset (default 0) |

#### Response fields

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `podcast_show_id` | int64 | Show id; pass to `transcripts` |
| `name` | string | Show name |
| `publisher` | string | Publisher (e.g. `Bloomberg`) |
| `feed_url` | string | RSS feed URL |
| `language` | string | ISO 639-1 language code |
| `episode_count` | int32 | Episodes discovered in the feed |
| `transcript_count` | int32 | Episodes with a transcript |
| `latest_episode_date` | string | Newest episode `YYYY-MM-DD` |
| `last_scanned_at` | string | ISO 8601 (UTC) last feed scan |

The response envelope also includes `pagination: { limit, offset }` and `request_id`.
