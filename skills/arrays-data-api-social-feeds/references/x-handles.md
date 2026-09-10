# X — Track (discover) a handle

`POST /api/v1/social-feeds/x/handles`

Explicitly start tracking an X/Twitter handle. An unknown handle is resolved on X and a subscription is created; a dormant handle is revived. Returns the first page of tweets plus an `outcome`.

This is the **only** endpoint that triggers on-demand X fetching. It is **per-user rate-capped** (daily) and each `discovered`/`revived` outcome is billed as a premium **discovery** unit. Use it once to onboard a handle, then read via `by-handle` / `search`; do not poll it.

#### Request body (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `handle` | string | yes | Twitter handle to track (no `@`, case-insensitive) |

#### Response

`data` is an array of tweet objects — the **first page** (most recent posts, up to 50) — using the same per-post shape as [`by-handle`](x-by-handle.md). The discovery `outcome` is returned in the response's `pagination` slot:

| Field | Type | Description |
|-------|------|-------------|
| `outcome` | string | `discovered` \| `revived` \| `already_tracked` (see below) |

`outcome` values:

| Value | Meaning | Tweets returned? | Billed as discovery unit? |
|-------|---------|------------------|---------------------------|
| `discovered` | Handle was unknown — resolved on X, subscription created, first page fetched | yes | yes |
| `revived` | Handle was dormant — subscription flipped active, first page fetched | yes | yes |
| `already_tracked` | Handle is already active (non-dormant) — nothing fetched; read via `by-handle` / `search` | no (empty `data`) | no (but still consumes a daily discovery-cap slot) |

The response envelope also includes `request_id`.

> Every call consumes one slot of the per-user daily discovery cap regardless of `outcome`. Only `discovered` / `revived` are billed as a premium discovery unit.

#### Errors

| Status | Code | When |
|--------|------|------|
| 400 | `VALIDATION_ERROR` | Missing/invalid body (e.g. bad handle format) |
| 429 | `DISCOVERY_QUOTA_EXCEEDED` | Per-user daily discovery limit reached |
