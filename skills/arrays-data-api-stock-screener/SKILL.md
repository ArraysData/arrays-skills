---
name: arrays-data-api-stock-screener
description: Calls Arrays REST APIs for stock screening and filtering — basic-info screener by country/exchange/industry/sector, event screener (IPO/splits/earnings), and financial/technical metrics screener. Use when the user wants to find, filter, or screen stocks by any criteria.
---


# Arrays Data API — Stock Screener

Company screener, basic-info screener (by country, exchange, industry, sector), event screener, financial metrics screener, and technical metrics screener.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Endpoints

- **Prefix**: `/api/v1/stocks/`

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `screener/basic-info/{sub}` | `basic-info-screener` | List tickers by a single basic-info dimension — `country` (ISO alpha-2), `exchange` (AMEX/NASDAQ/NYSE), `sector` (GICS), or `industry`. |
| GET | `screener/events` | `event-screener` | List tickers with a corporate event (`IPO Date`, `Split Date`, or `Earnings Date`) inside a Unix-time range. Splits/earnings capped at 1 year. |
| GET | `screener/financial-metrics` | `screener-financial-metrics` | At a single snapshot time, filter stocks by one financial metric (e.g. `PE_RATIO`, `ROE_TTM`, `REVENUE_GROWTH_YOY_TTM`) with optional `range_min`/`range_max` and sort. |
| GET | `screener/technical-metrics` | `screener-technical-metrics` | At a single snapshot time, filter stocks by one technical metric (e.g. `RSI_14`, `MA_20`, `PRICE_CHANGE_1M`, `BETA`) with optional `range_min`/`range_max` and sort. |
| GET | `screener/financial-metrics/timerange` | `screener-financial-metrics-timerange` | Same financial-metric filter as the snapshot version, but evaluated each day across `[start_time, end_time]`; results are grouped per date with optional per-day `limit`. |
| GET | `screener/technical-metrics/timerange` | `screener-technical-metrics-timerange` | Same technical-metric filter as the snapshot version, but evaluated each day across `[start_time, end_time]`; results are grouped per date with optional per-day `limit`. |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.

## Picking a metric: financial vs. technical

Each `metric_type` lives in exactly one endpoint. Use this table to route the request — if the metric isn't here, it isn't supported.

| Group | Endpoint | `metric_type` values |
|-------|----------|----------------------|
| Valuation (price-derived) | financial-metrics | `MARKET_CAP`, `PE_RATIO`, `PS_RATIO`, `PB_RATIO`, `DIVIDEND_YIELD`, `ENTERPRISE_VALUE`, `EV_EBITDA_RATIO` |
| TTM base fundamentals | financial-metrics | `REVENUE_TTM`, `NET_INCOME_TTM`, `EPS_TTM` |
| TTM profitability | financial-metrics | `ROA_TTM`, `ROE_TTM`, `ROIC_TTM` |
| MRQ margins | financial-metrics | `GROSS_MARGIN_MRQ`, `OPERATING_MARGIN_MRQ`, `NET_MARGIN_MRQ`, `FCF_MARGIN_MRQ` |
| MRQ balance-sheet ratios | financial-metrics | `CURRENT_RATIO_MRQ`, `QUICK_RATIO_MRQ`, `DEBT_TO_ASSETS_MRQ`, `DEBT_TO_EQUITY_MRQ`, `NET_WORKING_CAPITAL_MRQ` |
| R&D intensity | financial-metrics | `RD_TO_SALES_TTM` |
| Revenue growth | financial-metrics | `REVENUE_GROWTH_QOQ`, `REVENUE_GROWTH_YOY_QUARTERLY`, `REVENUE_GROWTH_YOY_TTM`, `REVENUE_GROWTH_YOY_ANNUAL` |
| EPS growth | financial-metrics | `EPS_GROWTH_QOQ`, `EPS_GROWTH_YOY_QUARTERLY`, `EPS_GROWTH_YOY_TTM`, `EPS_GROWTH_YOY_ANNUAL` |
| FCF growth | financial-metrics | `FCF_GROWTH_QOQ`, `FCF_GROWTH_YOY_QUARTERLY`, `FCF_GROWTH_YOY_TTM`, `FCF_GROWTH_YOY_ANNUAL` |
| Price change | technical-metrics | `PRICE_CHANGE_1D`, `PRICE_CHANGE_1W`, `PRICE_CHANGE_1M`, `PRICE_CHANGE_3M`, `PRICE_CHANGE_6M`, `PRICE_CHANGE_YTD`, `PRICE_CHANGE_1Y`, `PRICE_CHANGE_3Y`, `PRICE_CHANGE_5Y` |
| Volume | technical-metrics | `SHARES_VOLUME`, `DOLLAR_VOLUME`, `AVERAGE_DAILY_DOLLAR_VOLUME` |
| Simple moving averages | technical-metrics | `MA_5`, `MA_10`, `MA_20`, `MA_60`, `MA_120`, `MA_200` |
| Exponential moving averages | technical-metrics | `EMA_5`, `EMA_10`, `EMA_20`, `EMA_60`, `EMA_120`, `EMA_200` |
| Momentum | technical-metrics | `RSI_14` |
| MACD components | technical-metrics | `MACD_DIF`, `MACD_DEA`, `MACD_HIST` |
| Bollinger components | technical-metrics | `BOLLINGER_UPPER`, `BOLLINGER_MID`, `BOLLINGER_LOWER` |
| VWAP / risk | technical-metrics | `VWAP_DAY`, `BETA`, `VOLATILITY_20`, `VOLATILITY_60`, `VOLATILITY_90` |

Rule of thumb: if it comes from financial statements or price-vs-fundamentals ratios, use **financial-metrics**. If it comes from price/volume time series, use **technical-metrics**.

## Response format

**V2** (all screener endpoints):
```json
{ "success": true, "data": [...], "request_id": "..." }
```

**Error**:
```json
{ "success": false, "error": { "code": "...", "message": "..." }, "request_id": "..." }
```

## Example

```js
const base = process.env.ARRAYS_API_BASE_URL || 'https://data-tools.prd.space.id';
const apiKey = process.env.ARRAYS_API_KEY;
if (!apiKey) throw new Error('ARRAYS_API_KEY is not set');

// Screen for stocks with PE < 20 as of Dec 31, 2025, sorted by PE ratio (ascending)
const res = await fetch(
  `${base}/api/v1/stocks/screener/financial-metrics?snapshot=1767243599&metric_type=PE_RATIO&range_max=20&order_by=ASC`,
  { headers: { 'X-API-Key': apiKey } }
);
const json = await res.json();
if (!json.success) throw new Error(json.error?.message || 'API error');
const stocks = json.data; // Array of stock objects
```
