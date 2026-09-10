# Earnings Transcript

`GET /api/v1/stocks/earnings-transcript`

Full text of a company's earnings call, organized by speaker and section, for a specific fiscal period.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, MSFT) |
| `period_type` | string | Yes | `quarterly` (one transcript for the given `fiscal_quarter`) or `annual` (returns every available quarter of that fiscal year — up to 4 rows, `Q1`–`Q4` — **not** a single annual transcript) |
| `fiscal_year` | integer | Yes | Fiscal year — historical coverage from ~FY2005 (hard minimum 2005; earlier years return a validation error). e.g., 2024 |
| `fiscal_quarter` | string | No | Fiscal quarter: `Q1`, `Q2`, `Q3`, `Q4` — required when period_type is `quarterly` |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol (e.g., AAPL) |
| `quarter` | string | Fiscal period identifier, format `YYYYQ#` with **no space** (e.g. `2024Q1`, `2024Q4`). Note: this differs from `sec-earnings-release`, which uses `YYYYQQ` / `YYYY00`. |
| `date` | string | Earnings call date (`YYYY-MM-DD`) |
| `published_at` | string | Publish time as an RFC3339 UTC timestamp (e.g. `2024-10-31T20:54:36Z`). Empty string if unknown. |
| `transcript` | array | Array of transcript sections |

Each transcript section:

| Field | Type | Description |
|-------|------|-------------|
| `section` | string | Section name (e.g., "MANAGEMENT DISCUSSION SECTION") |
| `content` | array | Array of transcript entries |

Each transcript entry:

| Field | Type | Description |
|-------|------|-------------|
| `speaker` | string | Speaker name (e.g., "Arvind Krishna") |
| `title` | string | Speaker title/role (e.g., "CEO", "Analyst") |
| `content` | string | Transcript content/speech text |

---
