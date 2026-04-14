# Series

`GET series`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |
| `order` | string | no | Sort field |
| `ascending` | bool | no | Sort direction |
| `slug` | string | no | Filter by slug |
| `closed` | bool | no | Filter closed series |
| `recurrence` | string | no | Filter by recurrence type (e.g. `weekly`) |

**Response** — JSON array of series objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Series ID |
| `ticker` | string | Series ticker |
| `slug` | string | URL slug |
| `title` | string | Series title |
| `seriesType` | string | Type (e.g. `"single"`) |
| `recurrence` | string | Recurrence pattern (e.g. `"weekly"`) |
| `active` | bool | Whether series is active |
| `closed` | bool | Whether series is closed |
| `archived` | bool | Whether series is archived |
| `featured` | bool | Whether series is featured |
| `restricted` | bool | Whether series is restricted |
| `createdAt` | string | Creation timestamp (ISO 8601) |
| `updatedAt` | string | Last update timestamp (ISO 8601) |
| `events` | array | Array of nested event objects |
