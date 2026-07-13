# Ipo Calendar

`GET /api/v1/stocks/ipo-calendar`

Forward-looking IPO schedule from an upstream market-data vendor, with company details, expected pricing, and market information. Suitable for tracking *planned* IPO events.

**Not authoritative for historical IPOs**: this is a live passthrough of the vendor's planning calendar. To confirm whether a past listing actually happened (or to look up SEC filings for a known company), use `ipo-confirmed-calendar` or check historical prices/company profiles via the respective market data/fundamentals skills instead.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from` | string | No | Start date in YYYY-MM-DD format (e.g., 2025-04-24) |
| `to` | string | No | End date in YYYY-MM-DD format (e.g., 2025-07-24) |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol |
| `date` | string | IPO date (YYYY-MM-DD) |
| `daa` | string | IPO date-time (ISO 8601) |
| `company` | string | Company name |
| `exchange` | string | Exchange (e.g., "NYSE") |
| `actions` | string | Upstream-provided status. Common values include `Expected`, `Priced`, `Withdrawn`. **Not reliable for historical entries** — ETF, OTC, and SPAC listings frequently remain `Expected` long after they have actually listed (e.g., spot Bitcoin ETFs like IBIT/FBTC/ARKB still show `Expected` for their 2024-01 launch). Treat `Expected` on a past `date` as "unknown", not "did not list". |
| `shares` | integer | Number of shares offered (may be null) |
| `price_range` | string | Expected price range (may be null) |
| `market_cap` | string | Expected market cap (may be null) |

---
