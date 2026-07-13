# Non-US company detail (profile)

`GET /api/v1/stocks/non-us/company/detail`

Company profile for a non-US listed equity keyed by dotted-suffix symbol such as `0700.HK` or `000660.KS`. The response schema differs from the US `company/detail` endpoint — field names below are authoritative.

> **Coverage is a curated subset.** Only a selected list of non-US symbols is currently supported (spanning exchanges such as HKEX `.HK`, KRX `.KS`, SIX `.SW`; many exchanges and tickers are not yet included). Don't assume an arbitrary dotted ticker resolves.

## Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Non-US ticker in `<TICKER>.<EXCHANGE_SUFFIX>` form (e.g. `0700.HK`, `9888.HK`, `000660.KS`). Case-sensitive — keep the suffix uppercase. The suffix is part of the symbol; the bare ticker (`0700`) will not resolve. |

## Response

**Each item in the `data` array:**

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Ticker with exchange suffix (e.g. `0700.HK`) |
| `company_name` | string | Company name |
| `currency` | string | Reporting / trading currency (e.g. `HKD`, `JPY`, `GBP`) |
| `cik` | string\|null | SEC CIK (typically `null` for non-US issuers) |
| `isin` | string\|null | ISIN identifier (may be `null`) |
| `cusip` | string\|null | CUSIP identifier (often `null` for non-US issuers, e.g. `000660.KS`) |
| `exchange_full_name` | string | Full exchange name (e.g. `Hong Kong Stock Exchange`) |
| `exchange` | string | Exchange short code (e.g. `HKSE`) |
| `industry` | string | Sub-industry |
| `sector` | string | Sector |
| `website` | string | Company website URL |
| `description` | string | Long-form company description |
| `ceo` | string | CEO name |
| `country` | string | ISO country code of incorporation/operations (e.g. `CN`, `JP`, `GB`) |
| `full_time_employees` | int | Full-time employee count |
| `phone` | string | Contact phone |
| `address` | string | Street address |
| `city` | string | City |
| `state` | string\|null | State / province (often `null` outside US) |
| `zip` | string\|null | Postal code (may be `null`, e.g. `000660.KS`) |
| `image` | string | Logo URL |
| `ipo_date` | string | IPO date (`YYYY-MM-DD`) |

The response envelope also includes `request_id`.

---
