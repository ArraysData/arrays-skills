# Persons

`GET /api/v1/persons`
`GET /api/v1/persons/{person_id}`

Person registry: list with filters, or one person by id. Both return the same person shape below.

### List

Paginated. Top-level path, not under the podcast prefix. All parameters optional.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | no | Exact person name, case-insensitive; matches `display_name` and `aliases` |
| `q` | string | no | Substring match, case-insensitive, over `display_name` and `aliases` |
| `affiliation` | string | no | Substring match on any `positions[].affiliation` |
| `person_id` | string | no | Exact id; also accepts the ids `transcripts` returns |
| `updated_since` | string | no | RFC3339 lower bound on `updated_at` |
| `created_by_pipeline` | boolean | no | One-way switch: `true` returns only pipeline-created persons, `false` is a no-op |
| `limit` | integer | no | Max results (1–200, default 10) |
| `offset` | integer | no | Pagination offset (default 0) |

### One person

`GET /api/v1/persons/{person_id}` — `person_id` is the canonical UUID (case-insensitive), a legacy id (`tw-19829693`, the form older transcripts carry), or a UUID that has since been merged into another; all resolve to the canonical record, whose `person_id` is the UUID. `data` is a one-element array. Unknown id → `400 NOT_FOUND`. No `pagination` in the envelope.

#### Response fields

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `person_id` | string | UUID |
| `display_name` | string | Canonical spelling |
| `sources` | string[] | Which pipelines have seen this person |
| `positions` | object[] | Roles held (below). Optional |
| `shows` | object[] | Shows appeared on, as host or guest (below). Optional |
| `socials` | object[] | Social accounts (below). Always present, may be `[]` |
| `external_ids` | object[] | Authoritative identifiers (below). Optional |
| `aliases` | string[] | Spelling variants, including misheard transcriptions. Optional |
| `bio` | string | Short biography, from the curated roster. Optional |
| `avatar_url` | string | Profile image URL, from the curated roster. Optional |
| `tags` | string[] | Classification labels (e.g. `fund_manager`), curated outside the pipeline. Optional |
| `first_seen_url` | string | URL where this person was first picked up |
| `created_at` | string | ISO 8601 (UTC) |
| `updated_at` | string | ISO 8601 (UTC) |

Each entry in `positions`:

| Field | Type | Description |
|-------|------|-------------|
| `position` | string | Job title |
| `affiliation` | string | Organization. Optional |

Each entry in `shows`:

| Field | Type | Description |
|-------|------|-------------|
| `platform` | string | Platform the show runs on |
| `show` | string | Show name |
| `role` | string | How the person took part in the show |
| `confirmed` | boolean | Whether the role is confirmed |

Each entry in `socials`:

| Field | Type | Description |
|-------|------|-------------|
| `platform` | string | Social platform |
| `handle` | string | Account handle, without `@` |
| `url` | string | Profile URL |
| `id` | string | Platform-side numeric id. Optional |

Each entry in `external_ids`:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Identifier scheme; treat as an open set |
| `value` | string | The identifier |

Optional fields are omitted rather than returned empty — `socials` is the exception and returns `[]` when the
person has no accounts.

The response envelope also includes `pagination: { limit, offset, has_more }` and `request_id`. There is no
total; page until `has_more` is `false`.
