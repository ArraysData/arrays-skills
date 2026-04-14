# ETF Info

`GET /api/v1/etf/info`

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | ETF symbol (uppercase, e.g., SPY, QQQ, IWM) |

**Response envelope:** `{ "success": true, "request_id": "...", "data": [ ... ] }`

Each object in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Ticker symbol, the unique identifier for the ETF listed on an exchange |
| `name` | string | The official full name of the fund |
| `description` | string | A summary of the ETF's investment objective, tracked index, and key features |
| `logo` | string | URL to the ETF logo image |
| `isin` | string | International Securities Identification Number; a unique code for identifying securities globally |
| `asset_class` | string | The primary category of assets the ETF invests in (e.g., "Equity") |
| `security_cusip` | string | A unique alphanumeric code used to identify securities, primarily in North America |
| `domicile` | string | The country or jurisdiction where the fund is legally registered (e.g., "US") |
| `website` | string | The URL link to the product's official detail page |
| `etf_company` | string | The fund family or company managing the ETF (e.g., "SPDR") |
| `expense_ratio` | float64 | The annual fee charged to investors to manage the fund (e.g., 0.0945 means 0.0945%) |
| `assets_under_management` | float64 | The total market value of the financial assets managed by the fund |
| `avg_volume` | int64 | The average number of shares traded daily over a specific period |
| `inception_date` | string | The date when the fund was launched and began trading |
| `nav` | float64 | Net Asset Value per share of the ETF |
| `nav_currency` | string | The currency in which the NAV is denominated (e.g., "USD") |
| `holdings_count` | int32 | The total number of individual securities held in the ETF portfolio |
| `updated_at` | string | Timestamp indicating when this data entry was last refreshed |
| `sectors_list` | array | Sector breakdown list showing how the fund's assets are distributed across industries |
| `sectors_list[].industry` | string | The specific sector category (e.g., "Technology", "Financial Services") |
| `sectors_list[].exposure` | float64 | The percentage weight of this sector in the total portfolio |

---
