# Tags

`GET tags`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |
| `order` | string | no | Sort field |
| `ascending` | bool | no | Sort direction |

**Response** — JSON array of tag objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Tag ID |
| `label` | string | Tag display name |
| `slug` | string | URL slug |
| `createdAt` | string | Creation timestamp (ISO 8601) |
| `updatedAt` | string | Last update timestamp (ISO 8601) |
