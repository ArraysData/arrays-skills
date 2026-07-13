# Discovery & endpoint catalog

## Discovery workflow

Before guessing a path, list the available endpoints and their exact parameter values:

```
GET /api/v1/crypto/analytics/query?path=/discovery/endpoints
```

Each element of `data` describes one endpoint:

```json
{
  "path": "/v1/btc/exchange-flows/inflow",
  "parameters": { "window": ["block", "day", "hour"], "exchange": ["binance", "..."] },
  "required_parameters": ["exchange"]
}
```

Use `path` (with or without `/v1`), pick values from `parameters`, and make sure every name in `required_parameters` is present in your `params`.

**Omitting a required parameter is not caught by the gateway** — it forwards to upstream, which rejects it, and you get a `VALIDATION_ERROR` ("upstream provider returned status 400"). Checking discovery's `required_parameters` first avoids this. Verified examples:
- `/btc/exchange-flows/inflow` requires `exchange`
- `/btc/miner-flows/outflow` requires `miner`
- `/btc/network-data/fees` requires nothing

## Endpoint catalog (~245 accessible)

Grouped by asset → category, roughly:

| Asset | Example categories |
|-------|--------------------|
| `btc` | network-data, network-indicator, market-indicator, market-data, flow-indicator, exchange-flows, miner-flows, inter-entity-flows, fund-data |
| `eth` | network-data, market-data, exchange-flows, fund-data, eth2 |
| `xrp` | network-data, market-data, entity-flows, flow-indicator, amm-data, dex-data |
| `trx` | network-data |
| `erc20` | network-data, exchange-flows |
| `stablecoin` | exchange-flows, network-data |

A few paths are documented upstream but not accessible on the current plan and return an authorization error — treat those as not available. The discovery endpoint is the source of truth for what this key can actually reach.
