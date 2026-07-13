# Basic-info screener endpoints

Four separate endpoints, each filtering by a different dimension. The query parameter name matches the endpoint suffix.

### `GET /api/v1/stocks/screener/basic-info/country?country={code}`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `country` | string | yes | ISO 3166-1 alpha-2 country code |
| `symbol_type` | string | no | Asset type: `stock` (non-ETF) or `etf`. Default `stock`. |

Accepted values (57): `AE`, `AR`, `AU`, `BE`, `BM`, `BR`, `BS`, `CA`, `CH`, `CI`, `CL`, `CN`, `CO`, `CR`, `CY`, `DE`, `DK`, `ES`, `FI`, `FR`, `GB`, `GG`, `GI`, `GR`, `HK`, `ID`, `IE`, `IL`, `IN`, `IS`, `IT`, `JE`, `JO`, `JP`, `KR`, `KY`, `KZ`, `LU`, `MC`, `MO`, `MX`, `MY`, `NL`, `NO`, `PA`, `PE`, `PH`, `SE`, `SG`, `TH`, `TR`, `TW`, `US`, `UY`, `VG`, `VN`, `ZA`

### `GET /api/v1/stocks/screener/basic-info/exchange?exchange={name}`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `exchange` | string | yes | Exchange name |
| `symbol_type` | string | no | Asset type: `stock` (non-ETF) or `etf`. Default `stock`. |

Accepted values: `AMEX`, `NASDAQ`, `NYSE` (3 listing buckets). ETFs are included when `symbol_type=etf` — the `AMEX` bucket in particular is dominated by NYSE Arca-listed ETFs (Arca is folded into `AMEX`).

### `GET /api/v1/stocks/screener/basic-info/sector?sector={name}`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `sector` | string | yes | Sector name (screaming snake case) |

Accepted values: `BASIC_MATERIALS`, `COMMUNICATION_SERVICES`, `CONSUMER_CYCLICAL`, `CONSUMER_DEFENSIVE`, `ENERGY`, `FINANCIAL_SERVICES`, `HEALTHCARE`, `INDUSTRIALS`, `REAL_ESTATE`, `TECHNOLOGY`, `UTILITIES`

### `GET /api/v1/stocks/screener/basic-info/industry?industry={name}`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `industry` | string | yes | Industry name (title case with spaces) |

154 accepted values. Examples: `Advertising Agencies`, `Aerospace And Defense`, `Airlines Airports And Air Services`, `Auto Manufacturers`, `Banks Regional`, `Biotechnology`, `Computer Hardware`, `Consumer Electronics`, `Drug Manufacturers General`, `Financial Capital Markets`, `Gold`, `Information Technology Services`, `Insurance Life`, `Internet Content And Information`, `Medical Devices`, `Oil And Gas Integrated`, `Railroads`, `Real Estate Services`, `Reit Residential`, `Renewable Utilities`, `Restaurants`, `Semiconductors`, `Software Application`, `Software Infrastructure`, `Solar`, `Steel`, `Telecommunications Services`, `Waste Management` (full list at `https://internal-data-tools.prd.space.id/docs/output/v1_stocks_screener_basic-info_industry_get.json`)

**Response fields** (each item in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock ticker symbol (e.g. `AAPL`) |
| `type` | string | Screener dimension used: `sector`, `industry`, `country`, or `exchange` |
| `value` | string | The value that was matched (e.g. `Technology`, `US`, `NASDAQ`) |
