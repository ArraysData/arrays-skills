---
name: arrays-data-api-social-feeds
description: Calls Arrays REST APIs for social feeds — posts from X/Twitter handles (history + recent), post lookup by URL, full-text search across the indexed corpus, handle entity metadata, and the currently-tracked accounts list. Use when the user asks for tweets from a specific account, recent posts from a handle, posts referenced by a URL, posts matching a query or phrase, metadata about an X/Twitter handle, or a list of accounts already in the tracking registry.
---


# Arrays Data API — Social Feeds

Social feed endpoints. Current coverage is X/Twitter (posts by handle, post lookup by URL, full-text search, handle entity lookup, and listing currently-tracked accounts). Additional source platforms may be added under this domain over time.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- Handles are case-insensitive and must be passed without the leading `@`.
- `by-handle` triggers an on-demand lookup for handles that aren't yet in the registry and adds them to tracking immediately; the first page (most recent posts) is returned synchronously, with new posts fetched going forward via incremental refresh. Historical backfill is NOT automatic — a freshly-discovered handle returns only recent posts, so don't assume older history will appear on its own. `entities/handle/{twitter_handle}` does NOT auto-create on miss — unknown handles return `NOT_FOUND`.
- `search` is Elasticsearch full-text search (BM25 over `full_text`) against the tracked-handle registry index — not a live X/Twitter search. For an untracked handle, call `by-handle` first to ingest it. With `q` present, results are BM25-ranked; with `q` omitted they're reverse-chronological. Anti-scrape rule: when both `q` and `handle` are empty, `since` is capped to the last 30 days.
- All time fields in the response are ISO 8601 strings (UTC); `since`/`until` query parameters are Unix seconds.

## Path prefix and endpoints

- **Prefix**: `/api/v1/social-feeds/x/`
- **Paths** (all GET):
  - `by-handle` — posts from a specific X/Twitter handle (history + recent)
  - `by-url` — look up a post by its URL
  - `search` — Elasticsearch full-text search over posts already ingested by Arrays (does NOT hit the live X API)
  - `entities/handle/{twitter_handle}` — handle entity / metadata
  - `entities/handles` — list currently tracked X/Twitter accounts (paginated)

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `by-handle` | `x-by-handle` | Posts from a specific X/Twitter handle (history + recent) |
| GET | `by-url` | `x-by-url` | Look up an X/Twitter post by its URL |
| GET | `search` | `x-search` | Elasticsearch full-text search across posts already ingested by Arrays |
| GET | `entities/handle/{twitter_handle}` | `x-entities-handle` | Handle entity / metadata for an X/Twitter account |
| GET | `entities/handles` | `x-entities-handles` | List currently tracked X/Twitter accounts (paginated) |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Choosing between `search` and `by-handle`

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
