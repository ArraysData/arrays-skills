---
name: arrays-data-api-social-feeds
description: Calls Arrays REST APIs for social feeds — posts from tracked X/Twitter handles (history + recent), post lookup by URL, full-text search across the indexed corpus, handle entity metadata, the currently-tracked accounts list, and starting tracking of a new handle (discovery). Use when the user asks for tweets from a specific account, recent posts from a handle, posts referenced by a URL, posts matching a query or phrase, metadata about an X/Twitter handle, a list of accounts already in the tracking registry, or to start tracking / discover a handle that isn't tracked yet.
---


# Arrays Data API — Social Feeds

Social feed endpoints. Current coverage is X/Twitter (posts by handle, post lookup by URL, full-text search, handle entity lookup, and listing currently-tracked accounts). Additional source platforms may be added under this domain over time.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.arrays.org`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- Handles are case-insensitive and must be passed without the leading `@`.
- Reads are store-only — `by-handle` and `search` never fetch from X on demand. `by-handle` returns posts for an already-**tracked** handle (active or dormant); an unknown/untracked handle returns `400 HANDLE_NOT_TRACKED`. `entities/handle/{twitter_handle}` likewise does NOT auto-create on miss — unknown handles return `NOT_FOUND`.
- `POST handles` is the **only** endpoint that fetches from X on demand: it starts tracking a handle (resolves an unknown one, revives a dormant one) and returns its first page + an `outcome`. It is per-user daily rate-capped and **billed as a premium "discovery" unit** — call it once to onboard a handle, then read via `by-handle`/`search`; don't poll it. Backfill is NOT automatic: a freshly-tracked handle returns only recent posts, older history is not guaranteed.
- `search` is Elasticsearch full-text search (BM25 over `full_text`) against the tracked-handle registry index. With `q` present, results are BM25-ranked; with `q` omitted they're reverse-chronological. Pass `sort` (`relevance` / `latest` / `hottest`) to force the ordering regardless of `q` — e.g. `sort=latest` for newest-first even with a query. Anti-scrape rule: when both `q` and `handle` are empty, `since` is capped to the last 30 days.
- All time fields in the response are ISO 8601 strings (UTC); `since`/`until` query parameters are Unix seconds.

## Endpoints

- **Prefix**: `/api/v1/social-feeds/x/` — all paths below are relative to it.

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `by-handle` | `x-by-handle` | Posts from a specific TRACKED X/Twitter handle (read-only, from store) |
| GET | `by-url` | `x-by-url` | Look up an X/Twitter post by its URL |
| GET | `search` | `x-search` | Elasticsearch full-text search across posts already ingested by Arrays (not live X) |
| GET | `entities/handle/{twitter_handle}` | `x-entities-handle` | Handle entity / metadata for an X/Twitter account |
| GET | `entities/handles` | `x-entities-handles` | List currently tracked X/Twitter accounts (paginated) |
| POST | `handles` | `x-handles` | Start tracking (discover) a handle — the **only** on-demand X fetch; rate-capped and **billed**. Resolves unknown / revives dormant; returns first page + `outcome` |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Choosing between `search`, `by-handle`, and `handles`

- **Handle not tracked yet** (`by-handle`/`search` returned `HANDLE_NOT_TRACKED`, or the account is absent from `entities/handles`): call `POST handles` once to start tracking it, then read via `by-handle`/`search`. This is the only path that fetches on-demand and is rate-capped and **billed as a premium discovery unit** — call it once to onboard, never loop it.
- **Text query across all tracked accounts** (e.g. "Nvidia mentions in the last 30 days"): use `search` with `q` + `since`. One request, server-side ranking.
- **Text query scoped to one handle**: `search?q=...&handle=...`.
- **Browse one handle's timeline** without text matching: `by-handle`.
- **Structured filter only** (e.g. all `original` posts from a handle, no text query): either works; `search` lets you omit `q` and use the filters alone.

## Python example

End-to-end "Nvidia mentions across the indexed corpus in the last 30 days":

```python
import os, time, requests

base = os.environ["ARRAYS_API_BASE_URL"]
key  = os.environ["ARRAYS_API_KEY"]
headers = {"X-API-Key": key}

since = int(time.time()) - 30 * 24 * 3600
r = requests.get(f"{base}/api/v1/social-feeds/x/search",
                 params={"q": "nvidia", "since": since, "limit": 50},
                 headers=headers)
body = r.json()
assert body["success"], body

for tweet in body["data"][:5]:
    print(tweet["twitter_handle"], "→", tweet["url"])
print(f"total returned: {len(body['data'])}")
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
