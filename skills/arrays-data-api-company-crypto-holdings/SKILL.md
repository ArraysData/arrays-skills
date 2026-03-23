---
name: arrays-data-api-company-crypto-holdings
description: Guides the agent to call Arrays REST APIs for company crypto holdings and transactions. Use when the user needs data about which companies hold crypto or their crypto transaction history.
---

# Arrays Data API — Company Crypto Holdings

**Domain**: `company_crypto_holdings`. Company crypto holdings and crypto transaction history.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE` env var (default `https://data-gateway.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Path prefix and endpoints

- **Prefix**: `/api/v1/tokens/`
- **Paths** (all GET):
  - `crypto-holdings` — company crypto holdings (e.g. MicroStrategy BTC holdings)
  - `crypto-transactions` — company crypto buy/sell transactions

## Parameters by endpoint

### Company crypto holdings (`crypto-holdings`)

Retrieve company cryptocurrency holdings filtered by token symbol with optional NAV/market cap ratio filtering.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token_symbol` | string | yes | Token symbol (e.g., BTC, ETH, SOL, BNB) |
| `limit` | integer | no | Maximum number of results (1-100) |
| `crypto_nav_to_market_cap_ratio_min` | number | no | Minimum NAV/market cap ratio (0-2) |
| `crypto_nav_to_market_cap_ratio_max` | number | no | Maximum NAV/market cap ratio (0-2) |

Supported tokens: `BTC`, `ETH`, `SOL`, `BNB` (case insensitive). Not supported: `USDT`, `USDC`.

**Response fields** (in `response.companies` array, standard format):

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Company stock ticker symbol |
| `company_name` | string | Company name |
| `country` | string | Company country |
| `token_holdings` | object | Detailed token holdings, e.g. `{ "BTC": { "amount": 214246 } }` |

### Company crypto transactions (`crypto-transactions`)

Retrieve cryptocurrency transactions from SEC filings for public companies.

**Request parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | no | Company stock symbol (uppercase, e.g. MSTR, COIN) |
| `crypto_ticker` | string | no | Cryptocurrency ticker (uppercase, e.g. BTC, ETH) |
| `transaction_type` | string | no | Transaction type |

**Response fields** (in `response.transactions` array, standard format):

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

## Example

```js
const base = process.env.ARRAYS_API_BASE || 'https://data-gateway.prd.space.id';
const apiKey = process.env.ARRAYS_API_KEY;
const res = await fetch(`${base}/api/v1/tokens/crypto-holdings?token_symbol=BTC`, {
  headers: { 'X-API-Key': apiKey },
});
const data = await res.json();
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
