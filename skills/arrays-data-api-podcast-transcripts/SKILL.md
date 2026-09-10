---
name: arrays-data-api-podcast-transcripts
description: Calls Arrays REST APIs for podcast data — episode transcripts with resolved speakers, the show catalog, and the person registry. Use when the user asks for a podcast transcript, who spoke on a podcast episode, which episodes feature a specific person, a show's metadata or transcript coverage, or details about a podcast host or guest.
---

# Arrays Data API — Podcast Transcripts

Podcast episode transcripts (official + ASR) with resolved speakers, the show catalog, and the person registry.

## Base URL and auth

- **Base**: `ARRAYS_API_BASE_URL` env var (default `https://data-tools.prd.arrays.org`)
- **Auth**: Send `X-API-Key: <key>` header on every request. Read the key from env `ARRAYS_API_KEY` or `.env` file.

## Response envelope

All endpoints return a unified JSON envelope:
```json
{ "success": true, "request_id": "...", "data": [ ... ], "pagination": { "limit": 10, "offset": 0 } }
```
- `data` is **always an array**. A valid query that matches nothing is `200` with an empty `data` array.
- `persons` also returns `has_more` in `pagination`. `transcripts` does too when called with an update window, and then `pagination.cursor` replaces `offset`; see `references/podcast-transcripts.md`.
- Always check `body["success"]` before accessing data.

On failure `data` is `null` and the reason is in `error` (`code`, `message`, `docs_url`):

| Code | Meaning |
|------|---------|
| `INVALID_PARAMETER` | A value did not resolve — unknown or ambiguous show name, or a name conflicting with `podcast_show_id` |
| `VALIDATION_ERROR` | A parameter is missing or out of range; `error.details[]` names the field |

## Endpoints

| Method | Path | File | Description |
|--------|------|------|-------------|
| GET | `/api/v1/other/podcast/shows` | `podcast-shows` | Show catalog: `podcast_show_id`, publisher, episode/transcript counts |
| GET | `/api/v1/other/podcast/transcripts` | `podcast-transcripts` | Episode transcripts with resolved speakers |
| GET | `/api/v1/persons` | `persons` | Person registry: names, aliases, positions, socials, shows appeared on |
| GET | `/api/v1/persons/{person_id}` | `persons` | One person by id — canonical UUID or a legacy id from `transcripts` |

> `persons` lives at the top level, not under the podcast prefix. Per-endpoint parameters and fields: `references/<file>.md`.

## Choosing an entry point

- **"How complete is a show"**: `shows` — `episode_count` vs `transcript_count`. Also the source of `podcast_show_id`.
- **"What was said on show X"**: `transcripts?podcast_show_name=<name>`, plus `date=YYYY-MM-DD` for one episode.
- **"Which episodes feature person Y"**: `transcripts?speaker=<name>`. For the shows rather than the episodes, `persons` returns `shows` with a `host`/`guest` role per show.
- **"Who was on this episode"**: read `hosts` / `guests` — they already exclude played-tape voices. Reading `resolved_speakers` directly instead means filtering out `presence: "archival"` yourself, and weighing `confidence` and `attribution_source`; see `references/podcast-transcripts.md`.
- **"What changed since I last looked"**: `transcripts?updated_after=<unix>&updated_before=<unix>` — every episode whose metadata, transcript or speaker attribution changed in the window, all shows at once, paged by `pagination.cursor`. No show or speaker filter needed.
- **"Who is person Y"**: `persons?name=<name>` — also matches misheard-spelling aliases; use `q=` for substring search. Positions and socials live here only.
- **"Who is this `person_id`"** (from a transcript's `resolved_speakers`, `hosts` or `guests`): `persons/{person_id}` — accepts legacy ids such as `tw-19829693` as well as UUIDs.

## Python example

"Find Torsten Slok's podcast appearances and print who else was on":

```python
import os, requests

base = os.environ["ARRAYS_API_BASE_URL"]
headers = {"X-API-Key": os.environ["ARRAYS_API_KEY"]}

r = requests.get(f"{base}/api/v1/other/podcast/transcripts",
                 params={"speaker": "Torsten Slok", "limit": 10},
                 headers=headers)
body = r.json()
assert body["success"], body

for ep in body["data"]:
    slots = (ep.get("resolved_speakers") or {}).values()
    names = {s["person_id"]: s["name"] for s in slots if s.get("person_id")}
    on_air = [names.get(pid, pid) for pid in (ep.get("hosts") or []) + (ep.get("guests") or [])]
    print(ep["podcast_show_name"], ep["date"], "→", ", ".join(on_air))
```
