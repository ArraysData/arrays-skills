# Already-covered data → use the normalized endpoint, not the passthrough

Some of this provider's data is already ingested by Arrays and served through dedicated, normalized endpoints (typed `camelCase` fields, validation, longer-lived storage, their own skills). For anything covered here, **use the dedicated endpoint** — the passthrough is a raw forward (snake_case, ~60s cache, upstream rate limits) meant for the long tail.

## On-chain indicators

Skill `arrays-data-api-crypto-metrics-and-screener`, endpoints `/api/v1/crypto/metrics/<name>`:

| Upstream analytics path | Use this Arrays endpoint instead |
|---|---|
| `…/market-indicator/mvrv` | `/api/v1/crypto/metrics/mvrv` |
| `…/market-indicator/realized-price` | `/api/v1/crypto/metrics/realized-price` |
| `…/network-indicator/nupl` | `/api/v1/crypto/metrics/nupl` |
| `…/market-indicator/sopr` | `/api/v1/crypto/metrics/sopr` |
| `…/market-indicator/stablecoin-supply-ratio` | `/api/v1/crypto/metrics/ssr` |
| `…/network-indicator/puell-multiple` | `/api/v1/crypto/metrics/puell-multiple` |
| `…/market-indicator/estimated-leverage-ratio` | `/api/v1/crypto/metrics/leverage-ratio` |
| `…/flow-indicator/exchange-whale-ratio` | `/api/v1/crypto/metrics/whale-ratio` |
| `…/flow-indicator/exchange-inflow-cdd` | `/api/v1/crypto/metrics/inflow-cdd` |
| `…/inter-entity-flows/miner-to-exchange` | `/api/v1/crypto/metrics/miner-to-exchange` |

## Exchange flows

Skill `arrays-data-api-crypto-exchange-flow`, endpoint `/api/v1/crypto/exchange-flows` (on the `data-tools` host — the legacy `data-gateway` host serves the same data at `/api/v1/tokens/exchange-flows`): covers BTC/ETH exchange `inflow` / `outflow` / `netflow`.

## When to use the passthrough even for these metrics

These ingested endpoints currently serve **`day`-granularity** snapshots and are ingested **mainly for BTC**. Reach for the passthrough when you need:
- the upstream's finer native granularity (`hour` / `block` / `min`), or a window the normalized endpoint doesn't expose;
- an asset beyond what's ingested;
- a raw upstream field that normalization drops.

## Not this provider

Crypto **futures** data (funding, open interest, long-short, taker volume) is served by `arrays-data-api-crypto-futures-data` from a *different* source — it is not part of this provider's surface, so don't route futures questions to the passthrough.
