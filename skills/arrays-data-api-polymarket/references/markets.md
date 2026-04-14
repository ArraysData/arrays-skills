# Markets

`GET markets`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | no | Results per page |
| `offset` | int | no | Pagination offset |
| `order` | string | no | Sort field. Supported values: `volume`, `volume24hr`, `volume1wk`, `volume1mo`, `volume1yr`, `liquidity`, `competitive`. `competitive` = closest to 50/50 first (sort only, no odds filter params exist). Note: `volume_num`, `created_at` are NOT valid. |
| `ascending` | bool | no | Sort direction |
| `id` | string | no | Filter by market ID |
| `slug` | string | no | Filter by slug |
| `clob_token_ids` | string | no | Filter by CLOB token IDs |
| `condition_ids` | string | no | Filter by condition IDs |
| `question_ids` | string | no | Filter by question IDs |
| `active` | bool | no | Filter active markets |
| `closed` | bool | no | Filter closed markets |
| `archived` | bool | no | Filter archived markets |
| `tag_id` | int | no | Filter by tag ID |
| `related_tags` | string | no | Filter by related tags |
| `liquidity_num_min` | number | no | Min liquidity |
| `liquidity_num_max` | number | no | Max liquidity |
| `volume_num_min` | number | no | Min volume |
| `volume_num_max` | number | no | Max volume |
| `start_date_min` | string | no | Min start date (ISO 8601) |
| `start_date_max` | string | no | Max start date (ISO 8601) |
| `end_date_min` | string | no | Min end date (ISO 8601) |
| `end_date_max` | string | no | Max end date (ISO 8601) |
| `cyom` | bool | no | Filter "Create Your Own Market" markets |
| `include_tag` | bool | no | Include tag data in response |

**Response** — JSON array of market objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Market ID |
| `question` | string | Market question text |
| `conditionId` | string | On-chain condition ID (hex) |
| `slug` | string | URL slug |
| `description` | string | Full market description |
| `outcomes` | string | JSON-encoded array of outcome names, e.g. `"[\"Yes\", \"No\"]"` |
| `outcomePrices` | string | JSON-encoded array of prices, e.g. `"[\"0.2165\", \"0.7835\"]"`. **Note**: This is a Gamma server cached midpoint snapshot with minutes of delay. For real-time prices, use CLOB `/price` or `/midpoint` endpoints. |
| `clobTokenIds` | string | JSON-encoded array of CLOB token IDs per outcome |
| `active` | bool | Whether market is active |
| `closed` | bool | Whether market is closed |
| `volume` | string | Total volume (string) |
| `volumeNum` | number | Total volume (number) |
| `liquidity` | string | Current liquidity (string) |
| `liquidityNum` | number | Current liquidity (number) |
| `volume24hr` | number | 24-hour volume |
| `volume1wk` | number | 1-week volume |
| `volume1mo` | number | 1-month volume |
| `volume1yr` | number | 1-year volume |
| `startDate` | string | Market start date (ISO 8601) |
| `endDate` | string | Market end date (ISO 8601) |
| `startDateIso` | string | Start date (YYYY-MM-DD) |
| `endDateIso` | string | End date (YYYY-MM-DD) |
| `image` | string | Market image URL |
| `icon` | string | Market icon URL |
| `featured` | bool | Whether market is featured |
| `new` | bool | Whether market is new |
| `archived` | bool | Whether market is archived |
| `restricted` | bool | Whether market is restricted |
| `negRisk` | bool | Whether market uses neg-risk framework |
| `acceptingOrders` | bool | Whether order book is accepting orders |
| `enableOrderBook` | bool | Whether order book is enabled |
| `orderPriceMinTickSize` | number | Minimum price tick size |
| `orderMinSize` | number | Minimum order size |
| `resolutionSource` | string | Source for market resolution |
| `createdAt` | string | Creation timestamp (ISO 8601) |
| `updatedAt` | string | Last update timestamp (ISO 8601) |
| `events` | array | Associated event objects |
