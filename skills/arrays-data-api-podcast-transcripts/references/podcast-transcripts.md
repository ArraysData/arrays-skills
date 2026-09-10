# Podcast — Transcripts

`GET /api/v1/other/podcast/transcripts`

Episode transcripts with resolved speakers, sorted by `date` DESC. One of `podcast_show_id`, `podcast_show_name`, or `speaker` is required — unless you pass an update window (`updated_after` + `updated_before`), which may span all shows.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `podcast_show_id` | int64 | one-of | Show id from the `shows` endpoint |
| `podcast_show_name` | string | one-of | Show name, case-insensitive. `400 INVALID_PARAMETER` if unknown, ambiguous, or conflicting with `podcast_show_id` |
| `speaker` | string | one-of | Person name; matches `resolved_speakers`, not just publisher labels |
| `date` | string | no | Publish date `YYYY-MM-DD` |
| `include_raw` | boolean | no | Attach the raw source file as `raw_transcript` (default `false`). Payloads run 80 KB–34 MB — keep `limit` low when setting it |
| `limit` | integer | no | Max results (1–50, default 10) |
| `offset` | integer | no | Pagination offset (default 0). Not allowed with an update window |
| `updated_after` | int64 | window | Inclusive lower bound on `updated_at` (Unix seconds). Requires `updated_before` |
| `updated_before` | int64 | window | Exclusive upper bound on `updated_at` (Unix seconds); must exceed `updated_after` |
| `cursor` | string | no | Opaque continuation from `pagination.cursor`. Pass it back unchanged with the **same window and filters**; a different window → `400 INVALID_PARAMETER`. `limit` and `include_raw` may change between pages |

#### Update polling

With `updated_after` + `updated_before` the endpoint returns episode rows whose `updated_at` falls in `[after, before)`, ordered by `updated_at` ASC then `id` ASC, across all shows (or intersected with the usual filters). `updated_at` moves on episode metadata, transcript and attribution changes; show and person metadata have their own lifecycle. Page with `pagination.cursor` until `has_more` is `false`; start each new window without the old cursor. This is current-state polling, not a change log: overlap windows to catch delayed writes, and expect intermediate versions to coalesce. Roughly 2,000 rows were touched in a recent 14-day window.

#### Response fields

Each item in the `data` array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int64 | Stable Arrays record id (distinct from the publisher's `episode_id`) |
| `podcast_show_name` | string | Show name |
| `podcast_show_id` | int64 | Show id |
| `episode_id` | string | Episode GUID |
| `date` | string | Publish date `YYYY-MM-DD` |
| `transcript` | string | Normalized transcript, one line per turn: `[spk N @ seconds] text` |
| `transcript_type` | string | Source format: `vtt`, `srt`, `json`, `html`, `plain`, `deepgram-json` (ASR) |
| `transcript_source` | string | `official` or `asr` |
| `transcript_url` | string | Source file URL (audio URL for ASR rows). Omitted when unknown |
| `has_timestamps` | boolean | Whether turn timestamps come from the source |
| `resolved_speakers` | object | Map of `spk N` → resolved person (below). Only slots with confidence ≥ 0.4. Omitted when empty |
| `hosts` | string[] | `person_id`s of hosts, archival-only voices excluded. Omitted when empty |
| `guests` | string[] | `person_id`s of guests, archival-only voices excluded. Omitted when empty |
| `raw_transcript` | string | Raw source file; only when `include_raw=true` |
| `created_at` | string | ISO 8601 (UTC) ingestion time |
| `updated_at` | string | RFC 3339 (UTC); last change to episode metadata, transcript or attribution — the field update polling windows on |

Each value in `resolved_speakers` (position/affiliation: join `persons` via `person_id`):

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Verified canonical spelling |
| `person_id` | string | `tw-`/`ac-` = master table; `pc_` = auto-created. Omitted for a name the registry has no entry for |
| `role` | string | `host` or `guest` — how the voice functions in the audio. Always one of the two; played tape is marked on `presence`, not here |
| `confidence` | float | 0.4–1. `>= 0.7` use directly, `0.4–0.7` display with caution |
| `attribution_source` | string | Evidence for the mapping; values below |
| `presence` | string | `evidenced` or `archival`; values below. Filter **out** `archival` when you want the people who were on the show |

#### `presence` values

| Value | Meaning |
|-------|---------|
| `evidenced` | Judged to be taking part in this episode: self-introduced, introduced, or in dialogue |
| `archival` | Judged to be played tape or a quote from elsewhere, not a participant. Roughly 4–5% of slots, nearly all `role: guest` |

`hosts` / `guests` already exclude anyone whose slots are all `archival` — prefer them for "who was on this
episode". When reading `resolved_speakers` directly, filter **out** `presence == "archival"`.

`archival` is a best-effort judgement, not a guarantee: a played clip can still come back `evidenced`. The
weak spot is `attribution_source: title`, which never yields `archival` — someone named only in the episode
title can surface as an `evidenced` guest at high confidence. Treat `title` slots as unverified.

#### `attribution_source` values

| Value | Meaning |
|-------|---------|
| `title` | **Legacy, no longer produced; still on older rows.** The episode title named the person, with no transcript binding — merely-discussed people can carry it at high confidence, and it never yields `archival`. Weakest source |
| `intro_selfstated` | The person stated their own name |
| `intro_introduced` | Another voice introduced them |
| `signoff` | A closing credit named who spoke |
| `websearch` | Spelling and role confirmed against the web |
| `adjudicated` | Same-name collision resolved by the disambiguation step |

Sorted by `date` DESC. The response envelope also includes `pagination: { limit, offset }` and `request_id`.
