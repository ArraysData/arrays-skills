# Arrays Data API — Reference

## Spec file naming

Per-path OpenAPI specs are served by the gateway at `{BASE_URL}/docs/output/{filename}.json`.

**Naming rule**:

1. Take the path (e.g. `/api/v1/stocks/company/list`).
2. Strip the leading `/api/` prefix.
3. Replace `/` with `_`.
4. Append `_{method}.json` (e.g. `_get.json`, `_post.json`).

Example: path `/api/v1/stocks/company`, method GET -> `v1_stocks_company_get.json`.

Example: path `/api/v1/crypto/trading-pair`, method GET -> `v1_crypto_trading-pair_get.json`.

## Domain -> skill directory

| sdkhub Category | Skill directory under `by-domain/` |
|------------------|------------------------------------|
| equity_fundamentals | equity-fundamentals |
| equity_estimates_and_targets | equity-estimates-and-targets |
| equity_ownership_and_flow | equity-ownership-and-flow |
| equity_events_calendar | equity-events-calendar |
| etf_fundamentals | etf-fundamentals |
| macro_and_economics_data | macro-and-economics |
| spot_market_price_and_volume | spot-market-price-and-volume |
| company_crypto_holdings | company-crypto-holdings |
| crypto_futures_data | crypto-futures-data |
| crypto_exchange_flow | crypto-exchange-flow |
| crypto_technical_metrics / crypto_screener | crypto-metrics-and-screener |
| stock_screener | stock-screener |
| stock_technical_metrics | stock-technical-metrics |
| ask | ask |
| polymarket_markets | polymarket-markets |
| polymarket_pricing | polymarket-pricing |

## Full API index

See `API_INDEX.md` in this directory for a complete table listing each endpoint with path, method, spec_file, domain, and summary.
