# Earnings Transcript

`GET /api/v1/stocks/earnings-transcript`

Full text of a company's earnings call, organized by speaker and section, for a specific fiscal period.

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol (e.g., AAPL, MSFT) |
| `period_type` | string | Yes | Period type: `annual` or `quarterly` |
| `fiscal_year` | integer | Yes | Fiscal year (minimum: 2005, e.g., 2024) |
| `fiscal_quarter` | string | No | Fiscal quarter: `Q1`, `Q2`, `Q3`, `Q4` — required when period_type is `quarterly` |

**Response fields** (each object in `data[]`)

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol (e.g., AAPL) |
| `quarter` | string | Fiscal period identifier (e.g., "2024 Q1" for quarterly, "2024" for annual) |
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
