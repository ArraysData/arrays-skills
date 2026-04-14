# Reference File Template

Copy this template for each endpoint. Save as `references/{file-slug}.md` where `{file-slug}` matches the `File` column in the SKILL.md endpoint table.

**How to populate this template:**

1. Set up environment variables to call the API:
   ```bash
   export ARRAYS_API_BASE_URL=https://data-tools.prd.space.id
   export ARRAYS_API_KEY=2f21e762-fa1c-4eb8-a8ce-ec8c1e138812
   ```
2. Find the endpoint's API doc on Swagger: `https://data-tools.prd.arrays.org/swagger/index.html#/` — locate the matching endpoint and review its input parameters and response schema. Individual endpoint docs are also available as JSON at:
   ```
   https://data-tools.prd.space.id/docs/output/{version}_{path_with_underscores}_{method}.json
   ```
   e.g. `https://data-tools.prd.space.id/docs/output/v1_macro_treasury-rates_get.json`
3. Call the endpoint directly to verify the parameters and response fields match the doc.

---

```markdown
# {Endpoint Human Name}

`GET /api/v1/{asset-class}/{endpoint-path}`

{1-2 sentence description of what this endpoint returns and any critical behavior notes.}

<!-- Include special warnings or fallback patterns here if the endpoint has non-obvious behavior -->

## Parameters

<!-- OMIT this section if SKILL.md already has a "Common parameters" section that
     covers ALL of this endpoint's parameters. Only include when the endpoint has
     additional endpoint-specific parameters not in the common set. -->

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | yes | {Asset symbol} (e.g. `{EX_1}`, `{EX_2}`) |
| `start_time` | int64 | yes | Start time (Unix seconds) |
| `end_time` | int64 | yes | End time (Unix seconds). Must be > start_time |
| `limit` | int32 | no | Max results (default {DEFAULT}, max {MAX}) |

<!-- Add all endpoint-specific parameters -->
<!-- For enum params, list valid values: e.g., "`annual` or `quarter`" -->
<!-- Note defaults for optional params: e.g., "default 30" -->

## Response

{
  "success": true,
  "data": [
    {
      "{field_1}": "{example_value_1}",
      "{field_2}": 0.0001,
      "{field_3}": 1723507200
    }
  ]
}

<!-- Show a realistic response with actual field names and plausible values -->

**Each item in `data`:**

| Field | Type | Description |
|-------|------|-------------|
| `{field_1}` | string | {Description} |
| `{field_2}` | float64 | {Description} |
| `{field_3}` | int64 | {Description} |

<!-- For nested objects, add sub-tables: -->
<!-- **`{nested_object}` fields:** -->
<!-- | Field | Type | Description | -->

---
```
