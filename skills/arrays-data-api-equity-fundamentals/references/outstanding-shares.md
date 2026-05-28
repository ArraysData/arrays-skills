# Outstanding shares

`GET /api/v1/stocks/outstanding-shares`

Each `data` item is one **company-level snapshot** at a given date, with a per-share-class breakdown nested under `classes`.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | Stock symbol (canonical format: `AAPL`, `GOOG`, `BRK-B`) |
| `period_type` | string | yes | `quarterly` or `annual` (default `quarterly`) |
| `start_time` | int64 | yes | Unix seconds |
| `end_time` | int64 | yes | Unix seconds |
| `time_type` | string | no | `CALENDAR_END_DATE` (default), `FILING_DATE`, or `OBSERVED_AT` — same as other equity endpoints |

## Response fields

Each item in `data`:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Echoed query symbol |
| `company_name` | string | Issuer name (e.g. `Apple, Inc.`) |
| `date` | string | Report date (`YYYY-MM-DD`) — same as `calendar_end_date`, kept for backward compatibility |
| `calendar_end_date` | string | Last day of the reporting period (`YYYY-MM-DD`) |
| `filing_date` | string | Date results were communicated to the market (`YYYY-MM-DD`) |
| `observed_at` | int64 | Unix seconds when the data became observable — `filing_date + 1 day` |
| `period` | string | `quarterly` or `annual` |
| `fiscal_year` | string | Fiscal year |
| `fiscal_quarter` | string | `Q1`–`Q4` or `FY` |
| `unit` | string | Always `Million` |
| `total_outstanding` | float64 \| null | **Company-level** total outstanding shares |
| `classes` | array | Per-share-class breakdown (see below) |

Each item in `classes`:

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Class description (e.g. `Common Stock`, `Class A Common Stock`) |
| `ticker` | string \| null | Listed ticker for this class; `null` if non-listed |
| `shares` | float64 \| null | Shares outstanding for this class; `null` if no value available |
| `adr_description` | string \| null | ADR description (mostly null for US-domiciled issuers) |
| `adr_ratio` | float64 \| null | ADR conversion ratio |
| `adr_total_outstanding` | float64 \| null | ADR total outstanding |

## Notes

- **Multiple rows per period**: A company may report shares outstanding at the period-end date (from the 10-Q/10-K) and provide updated figures in subsequent filings before the next period. Expect more than one row per fiscal quarter or year, with slightly different `date` and `total_outstanding` values reflecting buybacks, issuances, or other changes between filings.
- Multi-class issuers (Alphabet, Berkshire, Meta) return one row per `date` with all classes nested. Both `GOOG` and `GOOGL` resolve to the same Alphabet record.
- Non-listed share classes (e.g. Alphabet's Class B) appear in `classes[]` with `ticker: null` and `shares: null`, but are still counted in the company `total_outstanding`.
- `BRK-B` and `BRK.B` both work as input and return the same data. The response echoes whichever format was sent.

## Example: single-class issuer (AAPL)

```json
{
  "symbol": "AAPL",
  "company_name": "Apple, Inc.",
  "date": "2026-01-16",
  "calendar_end_date": "2026-01-16",
  "filing_date": "2026-01-31",
  "observed_at": 1769904000,
  "period": "quarterly",
  "fiscal_year": "2026",
  "fiscal_quarter": "Q1",
  "unit": "Million",
  "total_outstanding": 14681.14,
  "classes": [
    {
      "description": "Common Stock",
      "ticker": "AAPL",
      "shares": 14681.14,
      "adr_description": null,
      "adr_ratio": null,
      "adr_total_outstanding": null
    }
  ]
}
```

## Example: multi-class with non-listed class (GOOG / Alphabet)

```json
{
  "symbol": "GOOG",
  "company_name": "Alphabet, Inc.",
  "date": "2025-10-22",
  "calendar_end_date": "2025-10-22",
  "filing_date": "2025-10-30",
  "observed_at": 1761868800,
  "period": "quarterly",
  "fiscal_year": "2025",
  "fiscal_quarter": "Q3",
  "unit": "Million",
  "total_outstanding": 12067,
  "classes": [
    { "description": "Class C Capital Stock",  "ticker": "GOOG",  "shares": 5407, "adr_description": null, "adr_ratio": null, "adr_total_outstanding": null },
    { "description": "Class A Common Stock",   "ticker": "GOOGL", "shares": 5818, "adr_description": null, "adr_ratio": null, "adr_total_outstanding": null },
    { "description": "Alphabet Inc. Class B",  "ticker": null,    "shares": null, "adr_description": null, "adr_ratio": null, "adr_total_outstanding": null }
  ]
}
```

## Example: multi-class (BRK-B / Berkshire)

```json
{
  "symbol": "BRK-B",
  "company_name": "Berkshire Hathaway, Inc.",
  "date": "2025-10-20",
  "calendar_end_date": "2025-10-20",
  "filing_date": "2025-11-04",
  "observed_at": 1762300800,
  "period": "quarterly",
  "fiscal_year": "2025",
  "fiscal_quarter": "Q3",
  "unit": "Million",
  "total_outstanding": 1373.343149,
  "classes": [
    { "description": "Class A Convertible Common Stock", "ticker": "BRK.A", "shares": 0.52301,    "adr_description": null, "adr_ratio": null, "adr_total_outstanding": null },
    { "description": "Class B Common Stock",             "ticker": "BRK.B", "shares": 1372.820139, "adr_description": null, "adr_ratio": null, "adr_total_outstanding": null }
  ]
}
```
