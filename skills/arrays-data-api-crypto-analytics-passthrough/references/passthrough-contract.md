# Passthrough contract — path, params, response, errors

## How `path` works

- Must start with `/` and use only letters, digits, `/`, `-`, `_`. No `..`, no `//`, max 256 chars. (SSRF guard — the host is fixed server-side; you only choose the path.)
- A leading `/v1` is **optional and auto-stripped**. Discovery returns paths like `/v1/btc/network-data/fees`; paste them verbatim or drop the `/v1` — both resolve to the same endpoint.

## How `params` works

`params` is itself a query string, so in the request it must be URL-encoded as a single value. The gateway then:
- parses it, **forces `format=json`**, and **caps `limit` at 10000** (larger values are clamped);
- ignores any `path` smuggled inside `params` (the top-level `path` always wins).

Easiest correct approach: let your HTTP client encode it — pass `params` as one string value and the client percent-encodes the `&` and `=` inside it (see example below).

## Response format

Standard Arrays envelope. `data` is the passed-through upstream `result.data` array, where **each element is a free-form object whose fields vary per endpoint** (generic passthrough — not typed). Inspect the first element or consult discovery to learn the shape.

Field names come straight from upstream in **`snake_case`** (e.g. `inflow_total`, `fees_block_mean_usd`) — different from the normalized `camelCase` the dedicated skills expose (e.g. exchange-flow's `inflowTotal`). Don't assume the same field names when switching between this passthrough and a dedicated skill. A real `/btc/network-data/fees` response:

```json
{
  "success": true,
  "data": [
    {
      "date": "2026-06-21",
      "fees_block_mean": 0.01823314,
      "fees_block_mean_usd": 1168.47171313,
      "fees_reward_percent": 0.00580076,
      "fees_total": 2.44324063,
      "fees_total_usd": 156575.20955916
    }
  ],
  "request_id": "..."
}
```

Edge cases to handle defensively:
- **Non-standard results**: when the upstream `result` is not a `{data:[...]}` shape, the whole `result` object is returned as a **single element** of `data`. (For `/discovery/endpoints`, `result.data` *is* an array, so `data` is the list of endpoint descriptors directly.)
- **Empty / missing upstream data** comes back as `data: []`, never `null`. Don't assume a fixed length.

## Error handling

Upstream status is mapped to the standard error envelope (`{"success": false, "error": {"code", "message"}}`):

| Situation | HTTP | `error.code` |
|-----------|------|--------------|
| Bad request / invalid `params` / invalid `path` | 400 | `VALIDATION_ERROR` |
| Path/endpoint not found | 400 | `NOT_FOUND` |
| Rate limited | 429 | `RATE_LIMITED` |
| Upstream 5xx | 503 | `UNAVAILABLE` |
| Our key/plan rejected upstream (401/403) | 500 | `INTERNAL_ERROR` |
| Upstream timeout | 408 | `TIMEOUT` |

- `NOT_FOUND` → re-check the path against discovery (typo, wrong asset/category, or a missing required param, which forwards to upstream and comes back as `VALIDATION_ERROR` "upstream provider returned status 400").
- `INTERNAL_ERROR` here usually means the server-side key/plan can't reach that endpoint, not a problem with your request.

## Caching

Fully-successful responses are cached server-side for ~60s (keyed on path + normalized query). Identical repeat calls within a minute return the cached body — fine for reads, just don't expect sub-minute freshness.

## Python example

```python
import requests, os

base = os.environ["ARRAYS_API_BASE_URL"]
key = os.environ["ARRAYS_API_KEY"]
url = f"{base}/api/v1/crypto/analytics/query"
headers = {"X-API-Key": key}

# 1) Discover what's available (do this when unsure about a path)
disc = requests.get(url, params={"path": "/discovery/endpoints"}, headers=headers).json()
endpoints = disc["data"]  # list of {path, parameters, required_parameters}

# 2) Call a specific endpoint. Pass `params` as ONE query-string value —
#    requests percent-encodes the '&' and '=' inside it automatically.
resp = requests.get(
    url,
    params={
        "path": "/btc/exchange-flows/inflow",   # leading /v1 optional
        "params": "exchange=binance&window=day&limit=30",
    },
    headers=headers,
)
body = resp.json()
if body["success"]:
    rows = body["data"]          # free-form objects; shape varies per endpoint
    for row in rows[:3]:
        print(row)
else:
    print("error:", body["error"]["code"], body["error"]["message"])
```

---

*Contract verified live against `https://data-tools.prd.arrays.org` on 2026-06-22: discovery (245 endpoints), data calls with params, `/v1` auto-strip, `VALIDATION_ERROR` on bad path, `NOT_FOUND` on unknown path, and required-param forwarding all behave as documented.*
