---
name: arrays-data-api-social-feeds
description: Calls Arrays REST APIs for per-handle social feeds — posts from X/Twitter handles (history + recent), post lookup by URL, handle entity metadata, and the currently-tracked accounts list. Use when the user asks for tweets from a specific account, recent posts from a handle, posts referenced by a URL, metadata about an X/Twitter handle, or a list of accounts already in the tracking registry.
---


# Arrays Data API — Social Feeds

Per-handle social feed endpoints. Current coverage is X/Twitter (posts by handle, post lookup by URL, handle entity lookup, and listing currently-tracked accounts). Additional source platforms may be added under this domain over time.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.space.id`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Important notes

- This skill is handle-first. For keyword search, see "Keyword search via handle filtering" below.
- Handles are case-insensitive and must be passed without the leading `@`.
- `by-handle` will trigger an on-demand X API lookup for handles that aren't yet in the registry; full historical backfill happens in the background once anti-abuse thresholds (followers + age) are satisfied. `entities/handle/{twitter_handle}` does NOT auto-create on miss — unknown handles return `NOT_FOUND`.
- All time fields in the response are ISO 8601 strings (UTC); `since`/`until` query parameters are Unix seconds.

## Path prefix and endpoints

- **Prefix**: `/api/v1/social-feeds/x/`
- **Paths** (all GET):
  - `by-handle` — posts from a specific X/Twitter handle (history + recent)
  - `by-url` — look up a post by its URL
  - `entities/handle/{twitter_handle}` — handle entity / metadata
  - `entities/handles` — list currently tracked X/Twitter accounts (paginated)

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `by-handle` | `x-by-handle` | Posts from a specific X/Twitter handle (history + recent) |
| GET | `by-url` | `x-by-url` | Look up an X/Twitter post by its URL |
| GET | `entities/handle/{twitter_handle}` | `x-entities-handle` | Handle entity / metadata for an X/Twitter account |
| GET | `entities/handles` | `x-entities-handles` | List currently tracked X/Twitter accounts (paginated) |

> For detailed parameters, response fields, and examples for a specific endpoint, read `references/<file>.md` in this skill directory.


## Keyword search via handle filtering

To find tweets mentioning a keyword (e.g. "Nvidia", "NVDA"), pick a handle set, fetch their recent tweets via `by-handle`, and filter the `full_text` field client-side.

Two common ways to pick the handle set:
- **Explicit list**: user names the accounts (e.g. `["elonmusk", "VitalikButerin"]`).
- **Registry top-N**: call `entities/handles` (sorted by `followers_count` DESC) and take the top N as a proxy for "broad coverage."

## Python example

End-to-end "Nvidia mentions across the top 10 tracked handles in the last 30 days":

```python
import os, time, requests

base = os.environ["ARRAYS_API_BASE_URL"]
key  = os.environ["ARRAYS_API_KEY"]
headers = {"X-API-Key": key}

# 1. Top 10 handles from the registry (sorted by followers DESC).
r = requests.get(f"{base}/api/v1/social-feeds/x/entities/handles",
                 params={"limit": 10}, headers=headers)
body = r.json()
assert body["success"], body
handles = [h["twitter_handle"] for h in body["data"]]

# 2. Fetch the last 30 days of tweets from each, filter for the keyword.
since = int(time.time()) - 30 * 24 * 3600
keyword = "nvidia"   # case-insensitive substring match
hits = []
for handle in handles:
    r = requests.get(f"{base}/api/v1/social-feeds/x/by-handle",
                     params={"twitter_handle": handle, "since": since, "limit": 200},
                     headers=headers)
    body = r.json()
    if not body.get("success"):
        continue
    for tweet in body["data"]:
        if keyword in (tweet.get("full_text") or "").lower():
            hits.append({"handle": handle, "url": tweet["url"], "text": tweet["full_text"]})

print(f"{len(hits)} tweets mention {keyword!r}")
for h in hits[:5]:
    print(h["handle"], "→", h["url"])
```

## Full spec

Per-endpoint request/response schema: `GET {BASE}/docs/output/{spec_file}.json` (see parent `reference.md`).
