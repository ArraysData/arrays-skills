---
name: arrays-data-api-etf-fundamentals
description: Guides the agent to call Arrays REST APIs for ETF fundamentals (holdings, info, country/sector weightings, fund flow). Use when the user needs ETF composition, performance, or flow data.
---


# Arrays Data API — ETF Fundamentals

**Domain**: `etf_fundamentals`. ETF holdings, info, country/sector weightings, and fund flow.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Path prefix and endpoints

- **Prefix**: `/api/v1/etf/`
- **Paths** (all GET):
  - `holdings` — ETF holdings (top constituents)
  - `info` — ETF basic information
  - `country-weightings` — allocation by country
  - `sector-weightings` — allocation by sector
  - `flow` — ETF fund flow / in/outflow data

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `info` | `info` | ETF Info |
| GET | `holdings` | `holdings` | ETF Holdings |
| GET | `country-weightings` | `country-weightings` | ETF Country Weightings |
| GET | `sector-weightings` | `sector-weightings` | ETF Sector Weightings |
| GET | `flow` | `flow` | ETF Fund Flow / In/Outflow |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).

## Example

```js
const base = process.env.ARRAYS_API_BASE_URL || 'https://data-tools.prd.space.id';
const apiKey = process.env.ARRAYS_API_KEY;
const res = await fetch(`${base}/api/v1/etf/holdings?symbol=SPY`, {
  headers: { 'X-API-Key': apiKey },
});
const data = await res.json();
```
