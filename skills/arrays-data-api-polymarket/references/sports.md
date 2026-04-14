# Sports

`GET sports`

No request parameters.

**Response** — JSON array of sport config objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Sport ID |
| `sport` | string | Sport code (e.g. `"nba"`, `"epl"`, `"mlb"`) |
| `image` | string | Sport image URL |
| `resolution` | string | Resolution source URL |
| `ordering` | string | Ordering type (e.g. `"home"`) |
| `tags` | string | Comma-separated tag IDs |
| `series` | string | Associated series ID |
| `createdAt` | string | Creation timestamp (ISO 8601) |
