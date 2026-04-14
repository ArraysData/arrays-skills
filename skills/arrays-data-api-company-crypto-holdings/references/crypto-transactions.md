# Company crypto transactions

`GET /api/v1/crypto/transactions`

Retrieve cryptocurrency transactions from SEC filings for public companies.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | no | Company stock symbol (uppercase, e.g. MSTR, COIN) |
| `crypto_ticker` | string | no | Cryptocurrency ticker (uppercase, e.g. BTC, ETH) |
| `transaction_type` | string | no | Transaction type |

**Response fields** (in `data` array):

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Transaction ID |
| `name` | string | Company name |
| `symbol` | string | Company stock symbol |
| `cik` | string | SEC CIK number |
| `filing_form` | string | SEC filing form type |
| `filing_date` | string | SEC filing date |
| `accession_number` | string | SEC accession number |
| `source_url` | string | SEC filing URL |
| `crypto_ticker` | string | Cryptocurrency ticker (e.g. BTC) |
| `transaction_type` | string | Transaction type (buy/sell) |
| `transaction_date` | string | Transaction date |
| `amount` | float64 | Amount of crypto transacted |
| `price_usd` | float64 | Price per unit in USD |
| `total_value_usd` | float64 | Total transaction value in USD |
| `created_at` | string | Record creation timestamp |
| `updated_at` | string | Record update timestamp |
