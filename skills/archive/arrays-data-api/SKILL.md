---
name: arrays-data-api
description: Overview of Arrays Data REST APIs covering stocks, crypto, ETFs, macro, and screening data. Use this skill as a fallback when no specific domain skill matches, or when the user needs a general API overview, authentication help, or cross-domain guidance.
---

# Arrays Data API — Overview

Arrays provides REST APIs for financial data across multiple domains. Each domain has a dedicated skill with endpoint details and parameter documentation. Use the domain-specific skill for best results.

## Available domain skills

| Domain | Skill name | Use when the user asks for |
|--------|------------|---------------------------|
| Equity fundamentals | `arrays-data-api-equity-fundamentals` | Company profile, financials, shares, KPI, options |
| Equity estimates | `arrays-data-api-equity-estimates-and-targets` | Analyst estimates, guidance, price target consensus/summary/news |
| Equity ownership | `arrays-data-api-equity-ownership-and-flow` | Institutional holdings, insider transactions, congress trades |
| Equity events | `arrays-data-api-equity-events` | Dividends, splits, earnings calendar, earnings transcripts, SEC earnings releases, IPO, M&A |
| ETF fundamentals | `arrays-data-api-etf-fundamentals` | ETF holdings, info, sector/country weightings, fund flow |
| Macro & economics | `arrays-data-api-macro-and-economics` | Treasury rates, economic calendar, forex, commodities, VIX |
| Spot market | `arrays-data-api-spot-market-price-and-volume` | Stock/crypto kline, OHLCV, market cap, supply, price |
| Company crypto | `arrays-data-api-company-crypto-holdings` | Company crypto holdings and transactions |
| Crypto futures | `arrays-data-api-crypto-futures-data` | Funding rate, open interest, long-short ratio |
| Crypto exchange flow | `arrays-data-api-crypto-exchange-flow` | Exchange inflow/outflow |
| Crypto metrics | `arrays-data-api-crypto-metrics-and-screener` | On-chain analytics, fear-greed, DeFi pools, token screening |
| Stock screener | `arrays-data-api-stock-screener` | Stock filtering by sector, valuation, financials, events |
| Stock technical | `arrays-data-api-stock-technical-metrics` | Market metrics, darkpool, analyst ratings |
| News | `arrays-data-api-ask` | Market news |
| Polymarket markets | `arrays-data-api-polymarket-markets` | Prediction markets, event outcomes, Polymarket search, market analytics, positions, trades, holders |
| Polymarket pricing | `arrays-data-api-polymarket-pricing` | Polymarket prices, odds, order books, spreads, price history |

## Base URL

Default: `https://data-tools.prd.space.id`. Override with env var `ARRAYS_API_BASE_URL`.

## Authentication

All endpoints require an API Key. Check these sources (first match wins):

| Source | How to read |
|--------|-------------|
| Env var `ARRAYS_API_KEY` | `process.env.ARRAYS_API_KEY` / `os.environ['ARRAYS_API_KEY']` |
| `.env` file in project root | Read `.env`, find `ARRAYS_API_KEY=...` |
| Agent-specific config | Depends on agent framework |

Attach the key to every request: `X-API-Key: <key>` header (preferred), or `Authorization: Bearer <key>`, or `?api_key=<key>`.

## Response format

All endpoints return a single unified envelope:

```json
{
  "success": true,
  "data": [{ ... }],
  "error": { "code": "NOT_FOUND", "message": "Symbol 'FAKE' not found" },
  "pagination": { "limit": 20, "offset": 0 },
  "request_id": "a1b2c3d4"
}
```

Rules:
- `data` is ALWAYS an array (single entity = array of one).
- `error` only present when `success: false`.
- `pagination` only present on paginated endpoints.
  - Offset-based: `{ "limit": 20, "offset": 0 }`
  - Cursor-based: `{ "limit": 20, "cursor": "abc", "has_more": true }`

Always check `success` before reading `data`.

## Symbol conventions

- **Stocks/ETF**: Standard ticker, uppercase (e.g. `AAPL`, `SPY`)
- **Crypto (spot)**: Token symbol (e.g. `BTC`, `ETH`, `SOL`)
- **Crypto (futures)**: Concatenated pair (e.g. `BTCUSDT`, `ETHUSDT`)
- **Trading pair lookup**: `GET /api/v1/crypto/trading-pair?base=BTC&quote=USDT`
- **Macro symbols**: Use symbol endpoints (e.g. `/api/v1/macro/forex/symbols`)

## Timestamps

All time parameters use **Unix seconds** (not milliseconds). Future timestamps are auto-clamped to now.

## Full endpoint index

See `API_INDEX.md` in this skill for a table listing every endpoint with path, method, spec file, and domain.

Per-endpoint OpenAPI spec: `GET {BASE}/docs/output/{spec_file}.json` (see `reference.md` for naming rule).
