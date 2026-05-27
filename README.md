# Arrays Skills

Skill definitions for [Arrays](https://arrays.org/), which is a unified data engine for intelligent finance. This repo is a Markdown skills that teach LLM agents (e.g., Claude, ChatGPT) how to call 114+ API endpoints provided by Arrays.

## What's in This Repo

| Directory | Contents |
|-----------|----------|
| `skills/` | 17 domain skills. Each skill is a `SKILL.md` describing API endpoints, parameters, and usage patterns. |
| `templates/` | Shared templates for authentication and response formatting. |

<details>
<summary>All 17 skills</summary>

| Skill | Description |
|-------|-------------|
| `arrays-data-api-company-crypto-holdings` | Corporate crypto holdings and transactions |
| `arrays-data-api-crypto-exchange-flow` | Exchange inflow/outflow (hourly/daily) |
| `arrays-data-api-crypto-futures-data` | Funding rates, open interest, long-short ratios, perp kline |
| `arrays-data-api-crypto-metrics-and-screener` | On-chain metrics, DeFi pools, fear-greed index, token screening |
| `arrays-data-api-equity-estimates-and-targets` | Analyst estimates, price targets, earnings guidance |
| `arrays-data-api-equity-events` | Dividends, splits, earnings calendar, transcripts, SEC filings, IPO, M&A |
| `arrays-data-api-equity-fundamentals` | Company financials, KPIs, executive info |
| `arrays-data-api-equity-ownership-and-flow` | Institutional holdings, insider/senate trades |
| `arrays-data-api-etf-fundamentals` | ETF holdings, sector weights, fund flow |
| `arrays-data-api-macro-and-economics` | Treasury rates, economic calendar, forex, commodities, VIX |
| `arrays-data-api-news` | Market news |
| `arrays-data-api-options` | Options chain, greeks, open interest |
| `arrays-data-api-polymarket` | Polymarket prediction markets and pricing |
| `arrays-data-api-social-feeds` | Per-handle X/Twitter feeds by handle or URL, handle entities |
| `arrays-data-api-spot-market-price-and-volume` | Stock/crypto kline, OHLCV, market cap |
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

Get your Arrays API key at [arrays.org](https://arrays.org/). The key is passed via the `X-API-Key` header on every request — see [templates/auth.md](templates/auth.md) for details.

## License

MIT License Copyright (c) 2026 Arrays Data