# Company crypto holdings

`GET /api/v1/crypto/holdings`

Retrieve company cryptocurrency holdings filtered by token symbol with optional NAV/market cap ratio filtering.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Token symbol (e.g., BTC, ETH, SOL, BNB) |
| `limit` | integer | no | Maximum number of results (1-100) |
| `crypto_nav_to_market_cap_ratio_min` | number | no | Minimum NAV/market cap ratio (0-2) |
| `crypto_nav_to_market_cap_ratio_max` | number | no | Maximum NAV/market cap ratio (0-2) |

Supported tokens: `BTC`, `ETH`, `SOL`, `BNB` (case insensitive). Not supported: `USDT`, `USDC`.

**Response fields** (in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Company stock ticker symbol |
| `company_name` | string | Company name |
| `country` | string | Company country |
| `token_holdings` | object | Detailed token holdings, e.g. `{ "BTC": { "amount": 214246 } }` |
