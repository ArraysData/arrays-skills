# Event Transcripts

`GET /api/v1/stocks/event-transcripts` (list)
`GET /api/v1/stocks/event-transcripts/{event_id}` (detail)

Transcripts for all covered corporate event types — earnings calls, shareholder/analyst meetings, conference presentations, sales & revenue calls, special situations, and guidance calls — queried by symbol + date range instead of fiscal period. The list endpoint returns event metadata; the detail endpoint returns the full transcript text. Coverage from 2004-01. Only events with an available transcript appear (not every meeting is transcribed).

## List

`GET /api/v1/stocks/event-transcripts`

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Yes | Stock symbol; US bare (e.g., AAPL), non-US dotted suffix (e.g., 0700.HK) |
| `event_type` | string | No | One of `Earnings`, `AnalystsShareholdersMeeting`, `ConferencePresentation`, `SalesRevenue`, `SpecialSituation`, `Guidance` (case-sensitive); omit for all types |
| `from` / `to` | int64 | No | Event-date range, Unix seconds (UTC); default ≈ last 90 days |
| `limit` | int32 | No | 1–100, default 20 |
| `offset` | int32 | No | ≥ 0, default 0 |

**Response fields** (each object in `data[]`, newest-first by `event_date`)

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | string | Event ID; pass to the detail endpoint for full text |
| `symbol` | string | Stock symbol |
| `event_type` | string | Same enum as the request parameter |
| `event_date` | string | Event date (`YYYY-MM-DD`, UTC) |
| `event_datetime` | string | Event start time, RFC3339 UTC |
| `headline` | string | Event title |
| `published_at` | string | Transcript publish time, RFC3339 UTC; empty string if unknown |
| `fiscal_year` | string, nullable | Fiscal year (`YYYY`); non-null for `Earnings` events only |
| `fiscal_quarter` | string, nullable | `Q1`–`Q4` (rarely `Q5`, an upstream label for companies that shifted their fiscal year end); non-null for `Earnings` events only |

The list envelope also carries `pagination` (`limit`, `offset`; no total) and `metadata.data_as_of` (Unix seconds). An empty page or a range with no events returns `200` with `data: []`; an unknown symbol returns `400 NOT_FOUND`.

## Detail

`GET /api/v1/stocks/event-transcripts/{event_id}`

**Request parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `event_id` | string (path) | Yes | Numeric event ID from the list endpoint |

**Response fields** — `data` is a single-element array; all list fields above plus:

| Field | Type | Description |
|-------|------|-------------|
| `transcript` | array | Transcript sections in original speaking order |

Each transcript section:

| Field | Type | Description |
|-------|------|-------------|
| `section` | string | Section name (e.g., "MANAGEMENT DISCUSSION SECTION") |
| `content` | array | Array of transcript entries |

Each transcript entry:

| Field | Type | Description |
|-------|------|-------------|
| `speaker` | string | Speaker name (e.g., "Tim Cook") |
| `title` | string | Speaker title/role (e.g., "CEO", "Analyst") |
| `content` | string | Transcript content/speech text |

---
