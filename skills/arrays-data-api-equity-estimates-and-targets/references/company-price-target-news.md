# Price target news

`GET /api/v1/stocks/company/price-target-news`

**Request parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | no | Stock symbol (e.g., META, AAPL) |
| `start_time` | integer | yes | Start time (Unix timestamp in seconds) |
| `end_time` | integer | yes | End time (Unix timestamp in seconds) |
| `limit` | integer | no | Maximum number of results (default: 20) |

**Response fields** (each item in `data` array)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol (e.g., `AAPL`) |
| `observed_at` | int64 | Observed timestamp (Unix seconds, may be omitted) |
| `publish_time` | string | Formatted time (`YYYY-MM-DD HH:mm:ss`, America/New_York, may be omitted) |
| `news_url` | string | Full URL to the news article |
| `news_title` | string | Title of the news article |
| `analyst_name` | string | Name of the analyst (may be omitted) |
| `analyst_company` | string | Company of the analyst (e.g., `Goldman Sachs`) |
| `price_target` | float64 | Price target value |
| `adj_price_target` | float64 | Adjusted price target value |
| `price_when_posted` | float64 | Stock price when the news was posted |
| `news_publisher` | string | Publisher name (e.g., `StreetInsider`) |
| `news_base_url` | string | Base URL of the publisher (e.g., `streetinsider.com`) |
