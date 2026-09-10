# Arrays Skills

Skill definitions for [Arrays](https://arrays.org/), a unified data engine for intelligent finance. These Markdown skills teach LLM agents how to call Arrays APIs across equities, ETFs, crypto, macro, news, and alternative data.

## What's in This Repo

| Directory | Contents |
|-----------|----------|
| `skills/` | 20 domain skills. Each has a `SKILL.md` describing API endpoints and usage patterns, plus detailed parameters and response fields in `references/`. |
| `templates/` | Shared templates for authentication and response formatting. |

<details>
<summary>All 20 skills</summary>

| Skill | Description |
|-------|-------------|
| `arrays-data-api-company-crypto-holdings` | Corporate crypto holdings and transactions |
| `arrays-data-api-crypto-analytics-passthrough` | On-chain analytics passthrough — ~245 upstream endpoints (network data, miner/entity flows, DEX/AMM) |
| `arrays-data-api-crypto-exchange-flow` | Exchange inflow/outflow (hourly/daily) |
| `arrays-data-api-crypto-futures-data` | Funding rates, open interest, long-short ratios, perp kline |
| `arrays-data-api-crypto-metrics-and-screener` | Token metadata, market cap, supply, on-chain metrics, fear-greed index, unlock schedules, token screening |
| `arrays-data-api-equity-estimates-and-targets` | Analyst estimates, price targets, earnings guidance |
| `arrays-data-api-equity-events` | Dividends, splits, earnings calendar, earnings and event transcripts, SEC earnings releases, IPO, M&A, equity offerings |
| `arrays-data-api-equity-fundamentals` | US and non-US company profiles, financial statements, SEC filings, executive compensation, shares float |
| `arrays-data-api-equity-ownership-and-flow` | Institutional holdings, insider/congress trades, short interest |
| `arrays-data-api-etf-fundamentals` | ETF holdings, sector weights, fund flow |
| `arrays-data-api-macro-and-economics` | Treasury rates, economic calendar, forex, commodities, VIX |
| `arrays-data-api-news` | Market news and symbol-filtered news with sentiment and relevance scores |
| `arrays-data-api-options` | Option contracts, OHLCV/VWAP, historical Greeks and implied volatility, option-chain snapshots |
| `arrays-data-api-podcast-transcripts` | Podcast transcripts, speaker attribution, show catalog, person registry, incremental transcript updates |
| `arrays-data-api-polymarket` | Prediction markets, prices, order books, positions, holders via public APIs |
| `arrays-data-api-semiconductor-price` | DRAM/NAND Flash spot & contract prices, memory cards, DXI index |
| `arrays-data-api-social-feeds` | X/Twitter posts by handle or URL, full-text search, handle entities, tracking discovery |
| `arrays-data-api-spot-market-price-and-volume` | Stock/crypto kline, OHLCV, previous close, unified market candles and trading-pair discovery |
| `arrays-data-api-stock-metrics` | Market cap, darkpool data, analyst ratings, market/technical metrics |
| `arrays-data-api-stock-screener` | Stock filtering (70+ filters), event screener |

</details>

## Usage

These skills work with any LLM-powered coding agent that supports Markdown context. Point your agent at the relevant `SKILL.md` files and it will know how to call the Arrays API.

### With Claude Code

Add this repo as a skill source in your Claude Code project. The agent will automatically select the relevant skill when answering financial data questions.

### With OpenAI Codex

Include the skill files as context when setting up your Codex agent. The Markdown format is directly compatible with Codex's instruction system.

### With Cursor / Windsurf / Other AI IDEs

Add the `skills/` directory to your project and reference the relevant `SKILL.md` in your AI assistant's context or rules.

### API Key

Get your Arrays API key at [arrays.org](https://arrays.org/). Set `ARRAYS_API_KEY` in your environment; Arrays requests use the `X-API-Key` header. `ARRAYS_API_BASE_URL` defaults to `https://data-tools.prd.arrays.org`. See [templates/auth.md](templates/auth.md) for details. The Polymarket skill calls public APIs and does not require an Arrays key.

## License

MIT License Copyright (c) 2026 Arrays Data
