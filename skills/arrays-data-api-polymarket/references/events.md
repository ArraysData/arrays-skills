# Events

`GET events`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |
| `order` | string | no | Sort field. Supported values: `volume`, `volume24hr`, `volume1wk`, `volume1mo`, `volume1yr`, `liquidity`, `competitive`. `competitive` = closest to 50/50 first (sort only). |
| `ascending` | bool | no | Sort direction |
| `id` | string | no | Filter by event ID |
| `slug` | string | no | Filter by slug |
| `tag_id` | int | no | Filter by tag ID |
| `tag_slug` | string | no | Filter by tag slug |
| `active` | bool | no | Filter active events |
| `closed` | bool | no | Filter closed events |
| `archived` | bool | no | Filter archived events |
| `featured` | bool | no | Filter featured events |
| `liquidity_min` | number | no | Min liquidity |
| `liquidity_max` | number | no | Max liquidity |
| `volume_min` | number | no | Min volume |
| `volume_max` | number | no | Max volume |
| `start_date_min` | string | no | Min start date (ISO 8601) |
| `start_date_max` | string | no | Max start date (ISO 8601) |
| `end_date_min` | string | no | Min end date (ISO 8601) |
| `end_date_max` | string | no | Max end date (ISO 8601) |
| `exclude_tag_id` | int | no | Exclude events with this tag ID |
| `include_chat` | bool | no | Include chat data in response |
| `include_template` | bool | no | Include template data in response |
| `recurrence` | string | no | Filter by recurrence type (e.g. `weekly`) |

**Response** — JSON array of event objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Event ID |
| `ticker` | string | Event ticker/slug identifier |
| `slug` | string | URL slug |
| `title` | string | Event title |
| `description` | string | Full event description |
| `resolutionSource` | string | Source URL for resolution |
| `startDate` | string | Start date (ISO 8601) |
| `creationDate` | string | Creation date (ISO 8601) |
| `endDate` | string | End date (ISO 8601) |
| `image` | string | Event image URL |
| `icon` | string | Event icon URL |
| `active` | bool | Whether event is active |
| `closed` | bool | Whether event is closed |
| `archived` | bool | Whether event is archived |
| `featured` | bool | Whether event is featured |
| `restricted` | bool | Whether event is restricted |
| `category` | string | Event category (e.g. `"Sports"`, `"Politics"`) |
| `liquidity` | number | Current liquidity |
| `volume` | number | Total volume |
| `openInterest` | number | Open interest |
| `volume24hr` | number | 24-hour volume |
| `volume1wk` | number | 1-week volume |
| `volume1mo` | number | 1-month volume |
| `volume1yr` | number | 1-year volume |
| `commentCount` | number | Number of comments |
| `markets` | array | Array of nested market objects |
