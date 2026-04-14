---
name: arrays-data-api-company-crypto-holdings
description: Guides the agent to call Arrays REST APIs for company crypto holdings and transactions. Use when the user needs data about which companies hold crypto or their crypto transaction history.
---


# Arrays Data API — Company Crypto Holdings

**Domain**: `company_crypto_holdings`. Company crypto holdings and crypto transaction history.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Path prefix and endpoints

- **Prefix**: `/api/v1/crypto/`
- **Paths** (all GET):
  - `holdings` — company crypto holdings (e.g. MicroStrategy BTC holdings)
  - `transactions` — company crypto buy/sell transactions

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `holdings` | `crypto-holdings` | Company crypto holdings |
| GET | `transactions` | `crypto-transactions` | Company crypto transactions |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Example

```js
const base = process.env.ARRAYS_API_BASE_URL || 'https://data-tools.prd.space.id';
const apiKey = process.env.ARRAYS_API_KEY;
const res = await fetch(`${base}/api/v1/crypto/holdings?symbol=BTC`, {
  headers: { 'X-API-Key': apiKey },
});
const data = await res.json();
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
