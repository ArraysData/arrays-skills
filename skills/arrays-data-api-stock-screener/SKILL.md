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

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `screener/basic-info/{sub}` | `basic-info-screener` | Basic-info screener endpoints |
| GET | `screener/events` | `event-screener` | Event screener |
| GET | `screener/financial-metrics` | `screener-financial-metrics` | Financial/technical metrics screener |
| GET | `screener/technical-metrics` | `screener-technical-metrics` | Financial/technical metrics screener |
| GET | `screener/financial-metrics/timerange` | `screener-financial-metrics-timerange` | Time range variants |
| GET | `screener/technical-metrics/timerange` | `screener-technical-metrics-timerange` | Time range variants |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


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
