---
name: arrays-data-api-crypto-analytics-passthrough
description: Forwards an arbitrary on-chain crypto analytics path + query string to the upstream provider through one Arrays passthrough route (GET /api/v1/crypto/analytics/query), unlocking ~245 endpoints. Use it for on-chain analytics that the dedicated crypto skills do NOT already cover — network-data (fees, hashrate, UTXO, addresses, supply), most network/market/flow indicators, miner flows, entity/inter-entity flows, fund-data, eth2, AMM/DEX data across BTC/ETH/XRP/TRX/ERC20/stablecoin — or when the user names a specific upstream metric/path, or asks what on-chain analytics endpoints are available. Do NOT use it when a dedicated endpoint already exists -- MVRV, NUPL, SOPR, realized price, SSR, Puell multiple, leverage ratio, whale ratio, inflow CDD, miner-to-exchange (use arrays-data-api-crypto-metrics-and-screener) and exchange inflow/outflow/netflow (use arrays-data-api-crypto-exchange-flow); crypto futures funding/open-interest/long-short come from a different source (use arrays-data-api-crypto-futures-data).
---

# Arrays Data API — Crypto Analytics Passthrough

**Domain**: `crypto_analytics`. A thin passthrough that forwards an arbitrary on-chain analytics **path** + **query string** to the upstream provider and returns the raw result through the standard Arrays envelope. One route unlocks the provider's full surface (~245 accessible endpoints) — use it for the long tail of on-chain metrics that have no dedicated Arrays skill.

> The upstream vendor is intentionally not named on this surface — route, params, and response type all say "analytics". Describe results as "on-chain analytics", never by a provider name.

## Prefer the normalized endpoints first

Some of this data is already ingested and served through dedicated, normalized endpoints (typed `camelCase` fields, validation, their own skills). **If the request is covered there, use those — not this passthrough**, which is a raw forward (snake_case, ~60s cache, upstream rate limits).

- **On-chain indicators** — MVRV, realized-price, NUPL, SOPR, SSR, Puell multiple, leverage ratio, whale ratio, inflow CDD, miner-to-exchange → `/api/v1/crypto/metrics/<name>` (skill `arrays-data-api-crypto-metrics-and-screener`).
- **Exchange inflow / outflow / netflow** (BTC/ETH) → `/api/v1/crypto/exchange-flows` (skill `arrays-data-api-crypto-exchange-flow`).

These are **`day`-granularity, mainly BTC**. Use the passthrough only for finer native granularity (`hour`/`block`/`min`), other assets, raw fields normalization drops, or any of the ~230 endpoints with no dedicated coverage. Full path↔endpoint mapping and the futures caveat: `references/normalized-endpoint-mapping.md`.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.arrays.org`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.
- **Tier**: **pro-tier only**. A free-tier key gets a tier/authorization error, not data.

## Endpoint

`GET /api/v1/crypto/analytics/query`

| Param | Required | Description |
|-------|----------|-------------|
| `path` | yes | Upstream analytics path, e.g. `/btc/exchange-flows/inflow`. Leading `/v1` optional (auto-stripped, so discovery paths paste in directly). SSRF-validated. |
| `params` | no | The upstream query string as **one URL-encoded value**, e.g. `exchange=binance&window=day` (≤4096). The gateway forces `format=json` and caps `limit` at 10000. Let your HTTP client encode it (pass as a single string). |

Full request/response contract, `snake_case` shape, error codes, caching, and a Python example: `references/passthrough-contract.md`.

## Discovery

Don't guess paths — list them with `path=/discovery/endpoints`. The response gives every endpoint with its allowed parameter values and `required_parameters` (omit a required param and it fails as `VALIDATION_ERROR`). ~245 endpoints across btc/eth/xrp/trx/erc20/stablecoin. Workflow, element shape, and the catalog: `references/discovery-and-endpoints.md`.
