# Public search

`GET public-search`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `q` | string | **yes** | Search query string |
| `limit_per_type` | int | no | Max results per entity type |
| `page` | int | no | Page number |
| `events_status` | string | no | Filter events by status |
| `events_tag` | string | no | Filter events by tag |
| `sort` | string | no | Sort field |
| `ascending` | bool | no | Sort direction |
| `search_tags` | bool | no | Include tags in search results |
| `search_profiles` | bool | no | Include profiles in search results |
| `exclude_tag_id` | int | no | Exclude events with this tag ID |
| `keep_closed_markets` | int | no | Include closed markets (0 or 1) |

**Response** — JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `events` | array | Array of matching event objects (same shape as `/events`) |
| `pagination` | object | Contains `hasMore` (bool) and `totalResults` (int). See Pagination section in SKILL.md for details. |
